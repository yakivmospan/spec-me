#!/usr/bin/env python3
"""Run claude-project's `sync_state.py` against throwaway repositories, and check what it did.

Usage: python3 claude_project_sync_state.py
"""
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "profiles/claude-project/skills/claude-project-sync/scripts/sync_state.py"
SYNC = ".claude-project/SYNC.md"


def repo(files):
    root = Path(tempfile.mkdtemp(prefix="sync-state-")).resolve() / "shop"
    for rel, text in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text)
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    return root


def run(root, *args):
    return subprocess.run([sys.executable, str(SCRIPT), *args, "--repo-root", str(root)],
                          capture_output=True, text=True)


SPEC = "# Checkout\n\n## Change history\n| Ticket | Change | Date |\n|---|---|---|\n| No ticket | First | 2026-01-10 |\n"


def link_adds_rows_and_keeps_old_ones(fails):
    root = repo({".specs/feature/checkout.md": SPEC, ".specs/INDEX.md": "generated\n",
                 ".specs/changes/cart/specs.feature.cart.md": SPEC,
                 ".specs/changes/cart/implementation-plan.md": "plan\n",
                 "docs/pricing.md": "prices\n", "print/sheet-v1.html": "<p>sheet</p>\n",
                 SYNC: "# Sync — last: 2026-01-12 10:00\nInstructions: abc123\n\n"
                       "| Project file | Repository · path | Last synced change |\n|---|---|---|\n"
                       "| docs.pricing.md | shop · docs/pricing.md | 2026-01-11 · First |\n"})
    out = run(root, "link", "--check")
    if (root / SYNC).read_text().count("| shop ·") != 1:
        fails.append("--check wrote SYNC.md")
    run(root, "link")
    text = (root / SYNC).read_text()
    for want in ("Instructions: abc123", "| docs.pricing.md | shop · docs/pricing.md | 2026-01-11 · First |",
                 "| specs.feature.checkout.md | shop · .specs/feature/checkout.md | never |",
                 "| specs.feature.cart.md | shop · .specs/changes/cart/specs.feature.cart.md | never |",
                 "| print.sheet-v1.html | shop · print/sheet-v1.html | never |"):
        if want not in text:
            fails.append(f"link: missing `{want}`\n{text}")
    for unwanted in ("INDEX.md", "implementation-plan"):
        if unwanted in text:
            fails.append(f"link: listed {unwanted}, which is not the project's material")
    again = run(root, "link")
    if "nothing to add" not in again.stdout or (root / SYNC).read_text() != text:
        fails.append("link is not stable on a second run")
    if "would add" not in out.stdout:
        fails.append(f"--check did not say what it would add:\n{out.stdout}")
    return root


def check_finds_an_edit_with_no_row(fails):
    root = repo({".specs/feature/checkout.md": SPEC, "docs/new.md": "new\n"})
    run(root, "link")
    (root / "docs/new.md").unlink()
    spec = root / ".specs/feature/checkout.md"
    later = time.mktime((2026, 1, 20, 12, 0, 0, 0, 0, -1))
    os.utime(spec, (later, later))
    (root / "docs/other.md").write_text("other\n")
    out = run(root, "check").stdout
    if "no row   .specs/feature/checkout.md — edited 2026-01-20, last change row 2026-01-10" not in out:
        fails.append(f"check missed an edit after the last change row:\n{out}")
    if "new      docs/other.md" not in out:
        fails.append(f"check missed a file with no row:\n{out}")
    if "gone     docs/new.md" not in out:
        fails.append(f"check missed a row whose file is gone:\n{out}")
    return root


def check_without_sync_md_says_so(fails):
    root = repo({"docs/a.md": "a\n"})
    out = run(root, "check")
    if out.returncode == 0 or "link this repo" not in out.stdout:
        fails.append(f"check with no SYNC.md passed silently:\n{out.stdout}")
    return root


if __name__ == "__main__":
    cases = [link_adds_rows_and_keeps_old_ones, check_finds_an_edit_with_no_row, check_without_sync_md_says_so]
    bad = 0
    for case in cases:
        fails = []
        root = case(fails)
        print(f"{'ok  ' if not fails else 'FAIL'} {case.__name__}")
        for f in fails:
            print(f"       {f}")
        bad += bool(fails)
        shutil.rmtree(root.parent, ignore_errors=True)
    print(f"\n{len(cases) - bad}/{len(cases)} cases passed")
    sys.exit(1 if bad else 0)
