# Model Cowork

> Give AI coding work a team, a plan, and a clear finish line.

[![Validation](https://img.shields.io/github/actions/workflow/status/Thatweirdguy1/Models-Cowork/validate.yml?branch=main&label=validation)](https://github.com/Thatweirdguy1/Models-Cowork/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Built for five hosts](https://img.shields.io/badge/hosts-5-5B5BD6)](#supported-hosts)

Model Cowork is an open, dependency-free coordination kit for AI-assisted software work. It helps decide **which available model should do which job**, keeps parallel workers from editing the same files, and asks every worker to return proof of what changed and how it was checked.

It supports **Codex**, **Claude Code**, **GitHub Copilot**, **Google Antigravity**, and **Ollama**. When apps cannot directly delegate to one another, it produces a portable handoff packet you can paste into the next tool.

## Why Model Cowork?

| Without coordination | With Model Cowork |
|---|---|
| One model does every task | Work is classified into planning, UI, backend, testing, review, and Git tasks |
| Workers may overwrite each other | Active workers must claim different files |
| Context is pasted repeatedly | A compact handoff carries goal, files, constraints, evidence, and risks |
| Strong models are spent on easy work | Fast or local models handle bounded tasks; hard work escalates deliberately |
| “Done” may only mean plausible | The integrator records checks that passed, failed, or were skipped |

## The 60-second version

Tell a supported coding app:

```text
Use Model Cowork in balanced mode.
Build a student dashboard with login, assignments, a calendar, dark mode, and tests.
```

Model Cowork should inspect the project, decide whether the work is safe to split, assign disjoint files, select from actually available models, gather exact verification evidence, and let one integrator assemble the result.

## What it routes

| Work type | Typical specialist | Good model traits |
|---|---|---|
| Architecture, migrations, difficult bugs | Lead / architect | Deep reasoning, long context |
| UI and responsive components | Frontend / UX | Coding plus visual understanding |
| APIs, auth, databases | Backend | Contract and debugging strength |
| Payments and security | Security reviewer | Careful reasoning and review |
| Tests and regressions | Tester | Repository exploration and precision |
| GitHub, branches, pull requests | Git specialist | Git tools and review discipline |
| Search, docs, renames | Fast worker | Low-latency, low-cost execution |

The registry contains candidate aliases for GPT, Claude, Gemini, Copilot, and local/cloud Ollama models. It discovers what is actually available before routing; a model name is never treated as guaranteed access.

## Modes

| Mode | Best for | Rule |
|---|---|---|
| `balanced` | Most features | Balance fit, speed, cost, tools, and privacy |
| `quality` | Architecture, security, payments, deep bugs | Prefer stronger reasoning and review |
| `economy` | Bounded/repetitive tasks | Prefer deterministic tools, fast models, and local options |
| `local-private` | Sensitive code or data | Use only local Ollama models; fail closed if none fit |

```text
Use Model Cowork in quality mode. Diagnose duplicate checkout charges; do not change live payment settings.

Use Model Cowork in economy mode. Remove unused imports and update related documentation.

Use Model Cowork in local-private mode. Review this private API using only local models.
```

## Supported hosts

| Host | Pack |
|---|---|
| Codex | Native plugin manifest, skill, specialist roles, marketplace support |
| Claude Code | Skill, specialist agents, `/model-cowork` command |
| GitHub Copilot | Agent skill plus lead, fast-worker, and reviewer profiles |
| Antigravity | Native plugin, skills, agents, workflow, rule, and hook structure |
| Ollama | Local model discovery and dependency-free router/chat adapter |

## Install

The Windows installer backs up an existing Model Cowork installation before replacing it. It never embeds API keys.

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1 -DryRun
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

See [Installation](docs/INSTALLATION.md) for host locations, restart guidance, and removal.

### Uploading into Claude Code

For Claude Code's plugin uploader, download [`Model-Cowork-Claude-Code-v1.0.1.zip`](https://github.com/Thatweirdguy1/Models-Cowork/releases/download/v1.0.1/Model-Cowork-Claude-Code-v1.0.1.zip). Do **not** upload GitHub's automatically generated “Source code (zip)” archive: it contains the whole multi-host repository, so `.claude-plugin/plugin.json` is not at the archive root.

## Help improve Model Cowork

Try it on one feature in a real repository. If it helps, please star the project and tell us which host, model, or handoff needs improvement in [Discussions](https://github.com/Thatweirdguy1/Models-Cowork/discussions) or an issue. Practical failure reports are especially valuable.

## Safety contract

Model Cowork intentionally does **not**:

- push, merge, deploy, or alter remote systems without your explicit approval;
- change payment settings or handle secrets casually;
- let two active workers own the same file;
- call cloud models in `local-private` mode;
- hide a failed or skipped check behind a “done” message.

The lead/integrator alone assembles work and may make the final commit or push after authorization.

## Handoffs that travel between apps

```json
{
  "objective": "Add secure Google sign-in without changing email/password login.",
  "assigned_files": ["src/auth.ts", "src/auth.test.ts"],
  "constraints": ["Preserve existing public API."],
  "completed_work": ["Login screen is finished."],
  "verification": ["Existing login tests pass."],
  "risks": ["OAuth redirect URI still needs configuration."],
  "expected_return": "Changed files, checks run, results, and remaining risks."
}
```

## Repository layout

```text
core/       Shared registry, router, schemas, tests, and handoff templates
packs/      Host-native packs for Codex, Claude, Copilot, Antigravity, and Ollama
install.ps1 Global Windows installer with backups
uninstall.ps1 Safe removal for Model Cowork-owned paths
docs/       Installation, contribution, and security guidance
```

## Validate locally

```powershell
python -m unittest discover -s .\core\tests -v
python .\core\model-cowork\model_cowork.py discover-ollama
python .\core\model-cowork\model_cowork.py route backend-api --host ollama --mode local-private
```

The core uses only Python’s standard library. If `python` is not on PATH, use any Python 3.11+ runtime.

## Contributing

Contributions are welcome—especially better routing fixtures, host compatibility improvements, clear examples, and model-registry updates grounded in real availability. Read [CONTRIBUTING.md](CONTRIBUTING.md) and report vulnerabilities privately as described in [SECURITY.md](SECURITY.md).

## License

Model Cowork is released under the [MIT License](LICENSE).
