---
holds: which files to ask about before touching, and nothing else — it loads every session
elsewhere:
  project-code-style-rules: naming convention, idiom, logging facade, error handling pattern, visibility
  project-workflow-rules: commit, branch, merge request, pipeline, CI, git hook, release, tag
---
# Sensitive paths

Always-on. Ask before touching any of these, and say why you need to. An edit here can break the
build, the release or generated code for everyone, and rarely looks dangerous in a diff.

{{SENSITIVE_PATHS — one bullet per path or glob that exists in this repository: build configuration, CI, signing keys and keystores, local machine config, lint and formatter config, migrations, infrastructure, sources that generate code. Add a short reason where it isn't obvious.}}
- `.agents/core/rules/**` — the rules every agent here follows; a change reaches every session
