#!/usr/bin/env python3
"""List what a TypeScript or Vue change left behind.

Compares the working tree (staged, unstaged and untracked files) with a git ref and reports:

  removed    names the change stopped declaring — functions, classes, types, top-level constants, deleted
             components and files — that nothing declares any more but something still mentions: code,
             templates, comments, docs or specs
  imports    anywhere in the repository: imports of files that do not exist, and of packages no
             package.json lists
  unused     in the files the change touched, and the files they used to import: exports nothing
             imports, files nothing imports, and files only tests import
  styles     in touched .vue files: classes a scoped or module <style> defines and the component never uses

With no commit to compare with (a new repository), or with --all, every source file is checked and the
removed section is skipped. Imports are read with patterns, not a compiler, so every hit is a lead to
check, not a verdict: a glob, a string path or a framework convention can use a file this cannot see.

Usage: python3 stale_refs.py [--base REF] [--all] [--repo-root PATH] [--exclude DIR ...] [--max-hits N]
"""
import argparse
import fnmatch
import json
import os
import re
import subprocess
import sys

CODE_EXTENSIONS = (".ts", ".tsx", ".mts", ".cts", ".js", ".jsx", ".mjs", ".cjs", ".vue")
RESOLVE_EXTENSIONS = CODE_EXTENSIONS + (".d.ts", ".json")
SKIPPED_DIRS = {
    ".git", ".cache", ".venv", "venv", "node_modules", "build", "out", "dist", "dist-ssr", "coverage",
    "__pycache__", ".next", ".nuxt", ".output", ".vite", "graphify-out",
}
OWN_FOLDER = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
MIN_NAME_LENGTH = 3
MAX_FILE_BYTES = 1_000_000
NODE_BUILTINS = {
    "assert", "async_hooks", "buffer", "child_process", "cluster", "console", "crypto", "dgram",
    "diagnostics_channel", "dns", "events", "fs", "http", "http2", "https", "inspector", "module", "net",
    "os", "path", "perf_hooks", "process", "querystring", "readline", "stream", "string_decoder", "test",
    "timers", "tls", "tty", "url", "util", "v8", "vm", "worker_threads", "zlib",
}
TEST_FILE = re.compile(r"(^|/)(__tests__|tests?|e2e|cypress)/|\.(spec|test|cy)\.[cm]?[jt]sx?$")
CONFIG_FILE = re.compile(r"(^|/)[^/]*\.config\.[cm]?[jt]s$|\.d\.ts$")

NAME = r"[A-Za-z_$][\w$]*"
IMPORT_FROM = re.compile(r"""\bimport\s+(type\s+)?([\w$*{}\s,]+?)\s*from\s*['"]([^'"]+)['"]""")
IMPORT_BARE = re.compile(r"""\bimport\s*['"]([^'"]+)['"]""")
EXPORT_FROM = re.compile(r"""\bexport\s+(?:type\s+)?(\*(?:\s+as\s+""" + NAME + r""")?|\{[^}]*\})\s*from\s*['"]([^'"]+)['"]""")
DYNAMIC_IMPORT = re.compile(r"""\bimport\s*\(\s*['"]([^'"]+)['"]\s*\)""")
MOCKED = re.compile(r"""\b(?:vi|jest)\.(?:mock|doMock|unmock|importActual|importMock)\s*(?:<[^>]*>)?\(\s*['"]([^'"]+)['"]""")
URL_REFERENCE = re.compile(r"""\bnew\s+URL\(\s*['"]([^'"]+)['"]\s*,\s*import\.meta\.url""")
GLOB_IMPORT = re.compile(r"""\bimport\.meta\.glob(?:Eager)?\s*(?:<[^>]*>)?\(\s*(\[[^\]]*\]|['"][^'"]+['"])""")
EXPORT_DECLARATION = re.compile(
    r"\bexport\s+(?:declare\s+)?(?:async\s+)?(?:abstract\s+)?"
    r"(?:function\s*\*?|class|interface|type|enum|const\s+enum|namespace|const|let|var)\s+(" + NAME + r")"
)
EXPORT_DEFAULT = re.compile(r"\bexport\s+default\b")
EXPORT_LIST = re.compile(r"\bexport\s+(?:type\s+)?\{([^}]*)\}(?!\s*from\b)")
# Declarations whose removal can leave a reference behind. A variable counts only at the top level
# or when exported: locals and parameters come and go with their function.
DECLARATION = re.compile(
    r"\b(?:function\s*\*?|class|interface|enum|namespace)\s+(" + NAME + r")|\btype\s+(" + NAME + r")\s*(?:<[^=]*>)?\s*="
)
VARIABLE = re.compile(r"^(?:export\s+)?(?:declare\s+)?(?:const|let|var)\s+(" + NAME + r")")
SCRIPT_BLOCK = re.compile(r"<script\b[^>]*>(.*?)</script>", re.S)
TEMPLATE_BLOCK = re.compile(r"<template\b[^>]*>(.*)</template>", re.S)
STYLE_BLOCK = re.compile(r"<style\b([^>]*)>(.*?)</style>", re.S)
CLASS_SELECTOR = re.compile(r"\.(-?[A-Za-z_][\w-]*)")
FOREIGN_SELECTOR = re.compile(r"(?::deep|::v-deep|:global|:slotted|::v-global|::v-slotted)\s*\([^)]*\)")


def git(root, *args, check=True):
    result = subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)
    if check and result.returncode != 0:
        sys.exit(f"stale_refs: git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout if result.returncode == 0 else None


def repo_root(override):
    if override:
        return os.path.abspath(override)
    return git(os.getcwd(), "rev-parse", "--show-toplevel").strip()


def read_text(path):
    try:
        if os.path.getsize(path) > MAX_FILE_BYTES:
            return None
        with open(path, "rb") as file:
            data = file.read()
    except OSError:
        return None
    if b"\0" in data[:4096]:
        return None
    return data.decode("utf-8", errors="replace")


def strip_comments(text):
    """Blank out // and /* */ comments, keeping strings, line breaks and so line numbers."""
    out, i, quote, length = [], 0, None, len(text)
    while i < length:
        char = text[i]
        if quote:
            out.append(char)
            if char == "\\" and i + 1 < length:
                out.append(text[i + 1])
                i += 1
            elif char == quote or (char == "\n" and quote != "`"):
                quote = None
        elif char in "'\"`":
            quote = char
            out.append(char)
        elif text.startswith("//", i):
            end = text.find("\n", i)
            i = length if end == -1 else end
            continue
        elif text.startswith("/*", i):
            end = text.find("*/", i + 2)
            end = length if end == -1 else end + 2
            out.append(re.sub(r"[^\n]", " ", text[i:end]))
            i = end
            continue
        else:
            out.append(char)
        i += 1
    return "".join(out)


def load_jsonc(path):
    text = read_text(path)
    if text is None:
        return {}
    try:
        return json.loads(re.sub(r",(\s*[}\]])", r"\1", strip_comments(text)))
    except ValueError:
        return {}


class Project:
    def __init__(self, root, excluded):
        self.root = root
        listed = git(root, "ls-files", "--cached", "--others", "--exclude-standard", "-z")
        self.files = sorted(
            path for path in listed.split("\0")
            if path and not self._skipped(path, excluded) and os.path.isfile(os.path.join(root, path))
        )
        self.file_set = set(self.files)
        self.aliases = self._aliases()
        self.packages = self._packages()

    def _skipped(self, path, excluded):
        parts = path.split("/")
        if any(part in SKIPPED_DIRS for part in parts[:-1]):
            return True
        if any(path == prefix or path.startswith(prefix + "/") for prefix in excluded):
            return True
        return os.path.realpath(os.path.join(self.root, path)).startswith(OWN_FOLDER + os.sep)

    def _aliases(self):
        """tsconfig `paths` as (prefix, directory) pairs: `@/*` -> ('@/', 'src/')."""
        aliases = []
        for path in self.files:
            name = os.path.basename(path)
            if not (name.startswith(("tsconfig", "jsconfig")) and name.endswith(".json")):
                continue
            options = load_jsonc(os.path.join(self.root, path)).get("compilerOptions") or {}
            base = os.path.normpath(os.path.join(os.path.dirname(path), options.get("baseUrl", ".")))
            for key, targets in (options.get("paths") or {}).items():
                for target in targets[:1]:
                    aliases.append((key.rstrip("*"), os.path.normpath(os.path.join(base, target.rstrip("*")))))
        return sorted(set(aliases), key=lambda alias: -len(alias[0]))

    def _packages(self):
        """Every package.json directory with the names it may import."""
        packages = {}
        for path in self.files:
            if os.path.basename(path) != "package.json":
                continue
            manifest = load_jsonc(os.path.join(self.root, path))
            names = {manifest.get("name")}
            for field in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
                names.update((manifest.get(field) or {}).keys())
            packages[os.path.dirname(path)] = names
        return packages

    def resolve(self, importer, specifier):
        """The repository file a specifier names, None when it names none, or '' for a package."""
        specifier = specifier.split("?")[0]
        if specifier.startswith("."):
            return self._find(os.path.join(os.path.dirname(importer), specifier))
        if specifier.startswith("/"):
            return self._find(specifier[1:]) or self._find(os.path.join("public", specifier[1:]))
        for prefix, directory in self.aliases:
            if prefix and specifier.startswith(prefix) or specifier == prefix.rstrip("/"):
                return self._find(os.path.join(directory, specifier[len(prefix):]))
        return ""

    def _find(self, path):
        path = os.path.normpath(path)
        stem = re.sub(r"\.[cm]?js$", "", path)
        candidates = [path] + [stem + extension for extension in RESOLVE_EXTENSIONS]
        candidates += [os.path.join(path, "index" + extension) for extension in RESOLVE_EXTENSIONS]
        found = next((candidate for candidate in candidates if candidate in self.file_set), None)
        return found or (path if os.path.exists(os.path.join(self.root, path)) else None)

    def package_listed(self, importer, specifier):
        if specifier.startswith(("node:", "virtual:", "~", "#", "@/", "bun:")) or "${" in specifier:
            return True
        parts = specifier.split("/")
        name = "/".join(parts[:2]) if specifier.startswith("@") else parts[0]
        if name in NODE_BUILTINS or (specifier.startswith("@") and len(parts) < 2):
            return True
        directory = os.path.dirname(importer)
        while True:
            if name in self.packages.get(directory, set()):
                return True
            if not directory:
                return not self.packages
            directory = os.path.dirname(directory)


class Module:
    """What one source file imports, re-exports and exports."""

    def __init__(self, project, path):
        self.path = path
        text = read_text(os.path.join(project.root, path)) or ""
        self.is_vue = path.endswith(".vue")
        script = "\n".join(SCRIPT_BLOCK.findall(text)) if self.is_vue else text
        self.script = strip_comments(script)
        template = TEMPLATE_BLOCK.search(text) if self.is_vue else None
        self.template = template.group(1) if template else ""
        self.styles = STYLE_BLOCK.findall(text) if self.is_vue else []
        self.imports = []          # (specifier, names imported: 'default', a name, or '*' for all)
        self.reexports = []        # (specifier, None for `export *`, or {exported name: original name})
        self.exports = {"default"} if self.is_vue else set()
        self.globs = [pattern for match in GLOB_IMPORT.finditer(self.script)
                      for pattern in re.findall(r"""['"]([^'"]+)['"]""", match.group(1))]
        self._read_imports()
        self._read_exports()

    def _read_imports(self):
        for match in IMPORT_FROM.finditer(self.script):
            self.imports.append((match.group(3), imported_names(match.group(2))))
        for pattern in (IMPORT_BARE, MOCKED, URL_REFERENCE):
            self.imports.extend((match.group(1), set()) for match in pattern.finditer(self.script))
        self.imports.extend((match.group(1), {"*"}) for match in DYNAMIC_IMPORT.finditer(self.script))

    def _read_exports(self):
        self.exports.update(match.group(1) for match in EXPORT_DECLARATION.finditer(self.script))
        if EXPORT_DEFAULT.search(self.script):
            self.exports.add("default")
        for match in EXPORT_LIST.finditer(self.script):
            self.exports.update(exported for _, exported in list_names(match.group(1)))
        for match in EXPORT_FROM.finditer(self.script):
            clause, specifier = match.group(1), match.group(2)
            if clause.startswith("{"):
                mapping = {exported: original for original, exported in list_names(clause[1:-1])}
                self.exports.update(mapping)
                self.reexports.append((specifier, mapping))
            elif " as " in clause:
                exported = clause.split()[-1]
                self.exports.add(exported)
                self.reexports.append((specifier, {exported: "*"}))
            else:
                self.reexports.append((specifier, None))


def list_names(inner):
    """`a, b as c, type d` -> [('a', 'a'), ('b', 'c'), ('d', 'd')]."""
    pairs = []
    for part in inner.split(","):
        words = re.sub(r"^\s*type\s+", "", part).split()
        if words:
            pairs.append((words[0], words[-1] if len(words) == 3 and words[1] == "as" else words[0]))
    return pairs


def imported_names(clause):
    names = {original for original, _ in list_names(re.search(r"\{([^}]*)\}", clause).group(1))} \
        if "{" in clause else set()
    rest = re.sub(r"\{[^}]*\}", "", clause).strip().strip(",").strip()
    if "*" in rest:
        names.add("*")
    elif rest:
        names.add("default")
    return names


def entry_points(project):
    """Files something outside the import graph starts: HTML pages, config files, package.json scripts."""
    entries = set()
    for path in project.files:
        if path.endswith(".html"):
            for source in re.findall(r"""<script\b[^>]*\bsrc=["']([^"']+)["']""", read_text(os.path.join(project.root, path)) or ""):
                found = project.resolve(path, source if source.startswith((".", "/")) else "./" + source)
                entries.add(found)
        elif CONFIG_FILE.search(path) or os.path.basename(path) == "package.json":
            for literal in re.findall(r"""['"]([\w@./-]+\.[cm]?[jt]sx?|[\w@./-]+\.vue)['"]""", read_text(os.path.join(project.root, path)) or ""):
                entries.add(project._find(os.path.join(os.path.dirname(path), literal)))
            if os.path.basename(path) == "package.json":
                for command in (load_jsonc(os.path.join(project.root, path)).get("scripts") or {}).values():
                    for word in command.split():
                        entries.add(project._find(os.path.join(os.path.dirname(path), word.strip("'\""))))
    return {entry for entry in entries if entry}


def build_graph(project):
    modules = {path: Module(project, path) for path in project.files if path.endswith(CODE_EXTENSIONS)}
    used = {path: set() for path in modules}
    importers = {path: set() for path in modules}
    broken = []
    for module in modules.values():
        for pattern in module.globs:
            resolved = project.resolve(module.path, pattern.split("*")[0]) if not pattern.startswith(".") else None
            base = os.path.normpath(os.path.join(os.path.dirname(module.path), pattern))
            for path in modules:
                if fnmatch.fnmatch(path, base) or (resolved and path.startswith(resolved)):
                    used[path].add("*")
                    importers[path].add(module.path)
        links = [(specifier, names) for specifier, names in module.imports]
        links += [(specifier, set()) for specifier, _ in module.reexports]
        for specifier, names in links:
            target = project.resolve(module.path, specifier)
            if target is None:
                if not any(char in specifier for char in "*${"):
                    broken.append((module.path, specifier, "no such file"))
            elif target == "":
                if not project.package_listed(module.path, specifier):
                    broken.append((module.path, specifier, "package not in package.json"))
            elif target in modules:
                used[target].update(names)
                importers[target].add(module.path)
    forward_reexports(project, modules, used)
    return modules, used, importers, broken


def forward_reexports(project, modules, used):
    """A name imported from a barrel counts as used in the file the barrel re-exports it from."""
    changed = True
    while changed:
        changed = False
        for module in modules.values():
            for specifier, mapping in module.reexports:
                target = project.resolve(module.path, specifier)
                if not target or target not in used:
                    continue
                wanted = used[module.path]
                if mapping is None:
                    forwarded = {"*"} if "*" in wanted else {name for name in wanted if name != "default"}
                else:
                    forwarded = {original for exported, original in mapping.items() if exported in wanted or "*" in wanted}
                if not forwarded <= used[target]:
                    used[target] |= forwarded
                    changed = True


def diff_changes(project, base):
    """Removed and added lines, removed lines per file, and the files the change touched or deleted."""
    removed, added, removed_by_file, deleted = [], [], {}, []
    current = None
    for line in git(project.root, "diff", "--unified=0", "--no-color", "--no-ext-diff", base).splitlines():
        if line.startswith("--- "):
            current = line[6:] if line.startswith("--- a/") else None
        elif line.startswith("+++ "):
            if line == "+++ /dev/null" and current:
                deleted.append(current)
        elif line.startswith("-"):
            removed.append(line[1:])
            if current:
                removed_by_file.setdefault(current, []).append(line[1:])
        elif line.startswith("+"):
            added.append(line[1:])
    touched = set(git(project.root, "diff", "--name-only", base).split("\n"))
    for path in git(project.root, "ls-files", "--others", "--exclude-standard").splitlines():
        touched.add(path)
        added.extend((read_text(os.path.join(project.root, path)) or "").splitlines())
    return removed, added, removed_by_file, deleted, {path for path in touched if path}


def declared_names(lines):
    names = set()
    for line in lines:
        code = line.split("//")[0]
        if code.lstrip().startswith(("*", "/*")):
            continue
        for match in DECLARATION.finditer(code):
            names.add(match.group(1) or match.group(2))
        variable = VARIABLE.match(code)
        if variable:
            names.add(variable.group(1))
    return {name for name in names if len(name) >= MIN_NAME_LENGTH}


def kebab(name):
    return re.sub(r"(?<!^)(?=[A-Z])", "-", name).lower()


def mention_pattern(name):
    """A plain lowercase word (`trigger`, `reset`) is everyday prose too, so only its code-shaped
    mentions count: called, reached with a dot, or in backticks. A component also counts as <kebab-case>."""
    escaped = re.escape(name)
    if re.fullmatch(r"[a-z]+", name):
        return re.compile(rf"(?:\.{escaped}\b|\b{escaped}\s*\(|`{escaped}\b)")
    if re.fullmatch(r"[A-Z][a-z0-9]+(?:[A-Z][a-z0-9]*)+", name):
        return re.compile(rf"(?<![\w$]){escaped}(?![\w$])|<{re.escape(kebab(name))}\b")
    return re.compile(rf"(?<![\w$]){escaped}(?![\w$])")


def removed_section(project, modules, removed, added, deleted):
    candidates = declared_names(removed) - declared_names(added)
    for path in deleted:
        if path.endswith(".vue"):
            candidates.add(os.path.basename(path)[:-4])
    still_declared = declared_names(
        line for path in project.files if path.endswith(CODE_EXTENSIONS)
        for line in (read_text(os.path.join(project.root, path)) or "").splitlines()
    ) | {os.path.basename(path)[:-4] for path in modules if path.endswith(".vue")}
    patterns = {name: mention_pattern(name) for name in sorted(candidates - still_declared)}
    for path in deleted:
        stem = re.sub(r"\.[^./]+$", "", path)
        patterns[path] = re.compile(re.escape(stem.split("/", 1)[-1]) + r"(?:\.[\w]+)?\b")
    hits = {name: [] for name in patterns}
    for path in project.files:
        for number, line in enumerate((read_text(os.path.join(project.root, path)) or "").splitlines(), start=1):
            for name, pattern in patterns.items():
                if pattern.search(line):
                    hits[name].append(f"{path}:{number}: {line.strip()[:160]}")
    return {name: found for name, found in hits.items() if found}


def unused_section(modules, used, importers, scope, entries):
    orphans, test_only, exports = [], [], {}
    for path in sorted(scope):
        if path not in modules or path in entries or TEST_FILE.search(path) or CONFIG_FILE.search(path):
            continue
        callers = importers[path]
        if not callers:
            orphans.append(path)
            continue
        if all(TEST_FILE.search(caller) for caller in callers):
            test_only.append(path)
        if "*" not in used[path]:
            unused = sorted(modules[path].exports - used[path])
            if unused:
                exports[path] = unused
    return orphans, test_only, exports


def styles_section(modules, scope):
    findings = []
    for path in sorted(scope):
        module = modules.get(path)
        if not module or not module.is_vue:
            continue
        used_text = module.template + "\n" + module.script
        for attributes, css in module.styles:
            if "scoped" not in attributes and "module" not in attributes:
                continue
            css = FOREIGN_SELECTOR.sub("", re.sub(r"url\([^)]*\)", "", strip_comments(css)))
            selectors = " ".join(re.findall(r"([^{}]+)\{", css))
            for name in sorted(set(CLASS_SELECTOR.findall(selectors))):
                if not re.search(rf"(?<![\w-]){re.escape(name)}(?![\w-])", used_text):
                    findings.append(f"{path}: .{name}")
    return findings


def print_section(title, lines, max_hits):
    if not lines:
        return
    print(f"\n{title}")
    for line in lines[:max_hits]:
        print(f"  {line}")
    if len(lines) > max_hits:
        print(f"  … {len(lines) - max_hits} more")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base", default="HEAD", help="git ref to compare the working tree with (default: HEAD)")
    parser.add_argument("--all", action="store_true", help="check every source file, not only the touched ones")
    parser.add_argument("--repo-root", help="repository root (default: found with git)")
    parser.add_argument("--exclude", nargs="*", default=[], help="directories to skip, relative to the root")
    parser.add_argument("--max-hits", type=int, default=20, help="lines shown per finding (default: 20)")
    args = parser.parse_args()

    project = Project(repo_root(args.repo_root), {os.path.normpath(path) for path in args.exclude})
    modules, used, importers, broken = build_graph(project)
    has_base = git(project.root, "rev-parse", "--verify", "--quiet", args.base + "^{commit}", check=False)
    stale = {}
    if has_base and not args.all:
        removed, added, removed_by_file, deleted, touched = diff_changes(project, args.base)
        scope = set(touched)
        for path, lines in removed_by_file.items():
            for match in IMPORT_FROM.finditer("\n".join(lines)):
                target = project.resolve(path, match.group(3))
                if target:
                    scope.add(target)
        for path in [path for path in scope if path in modules]:
            scope.update(project.resolve(path, specifier) for specifier, _ in modules[path].reexports)
        stale = removed_section(project, modules, removed, added, deleted)
    else:
        if not has_base:
            print(f"stale_refs: no commit {args.base} to compare with; checking every source file")
        scope = set(modules)

    broken = [f"{path}: '{specifier}' — {why}" for path, specifier, why in broken]
    orphans, test_only, exports = unused_section(modules, used, importers, scope, entry_points(project))
    styles = styles_section(modules, scope)
    if not (stale or broken or orphans or test_only or exports or styles):
        print("stale_refs: nothing left behind")
        return
    for name, hits in stale.items():
        print_section(f"removed: {name} — still mentioned {len(hits)} time(s)", hits, args.max_hits)
    print_section("imports: pointing at nothing", broken, args.max_hits)
    print_section("unused: files nothing imports", orphans, args.max_hits)
    print_section("unused: files only tests import", test_only, args.max_hits)
    print_section("unused: exports nothing imports",
                  [f"{path}: {', '.join(names)}" for path, names in exports.items()], args.max_hits)
    print_section("styles: classes the component never uses", styles, args.max_hits)


if __name__ == "__main__":
    main()
