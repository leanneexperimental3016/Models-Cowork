# Validation Report

Validated on Windows on 2026-08-28.

## Passed

- Seven dependency-free router tests: task scenarios, availability filtering, Ollama `:latest` aliases, local-private cloud exclusion, conflict rejection, ownership release, and registry uniqueness.
- Codex plugin validator passed for `1.0.0+codex.20260828145540`.
- All five copies of the Model Cowork skill passed the skill validator.
- Every JSON manifest, schema, registry, and template parsed successfully.
- Five host ZIPs contain their native manifest/directory at archive root.
- Global installer completed twice; the second run backed up all replaced Model Cowork targets.
- Codex reports `model-cowork@personal` installed and enabled.
- Claude Code skill, agents, command, and editable source are installed.
- Copilot skill and custom-agent profiles are installed.
- Antigravity native plugin is installed under its detected plugin directory.
- Ollama `/api/tags` discovery succeeded and local-private routing returned only local models.
- The personal Codex marketplace passes the official name helper and is encoded as UTF-8 without BOM.

## Verification boundaries

- Copilot and `agy` executables were not available on `PATH`; their filesystem installation is verified, but an in-app invocation requires restarting/opening those apps.
- No GitHub push, deployment, payment mutation, or destructive external action was performed.
- Start a new Codex/Claude/Copilot/Antigravity task after installation so each host reloads its skills and agents.

