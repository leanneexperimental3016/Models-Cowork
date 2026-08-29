# Installation

## Windows quick start

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1 -DryRun
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

The installer copies only Model Cowork-owned paths and creates timestamped backups under `%USERPROFILE%\.model-cowork\backups` before replacing an existing installation. Start a **new** task/session in each host after installation.

## Installed locations

| Host | Location |
|---|---|
| Codex | `%USERPROFILE%\plugins\model-cowork` and the personal marketplace |
| Claude Code | `%USERPROFILE%\.claude\skills\model-cowork`, agents, command, editable source |
| GitHub Copilot | `%USERPROFILE%\.copilot\skills\model-cowork` and custom-agent profiles |
| Antigravity | `%USERPROFILE%\.gemini\config\plugins\model-cowork` |
| Ollama adapter | `%USERPROFILE%\.model-cowork\ollama` |

The installer reports hosts whose executable is not on `PATH`. Their files were installed, but you should open/restart the app and test an invocation.

## Ollama

Ollama is optional. When running, Model Cowork queries `http://127.0.0.1:11434/api/tags` to discover model names.

```powershell
python $env:USERPROFILE\.model-cowork\ollama\model_cowork.py discover-ollama
```

`local-private` excludes cloud-tagged models and returns no route rather than silently sending work to a cloud provider.

## Uninstall

```powershell
powershell -ExecutionPolicy Bypass -File .\uninstall.ps1
```

Only Model Cowork-owned paths are removed. Marketplace history and backups remain intentionally recoverable.

