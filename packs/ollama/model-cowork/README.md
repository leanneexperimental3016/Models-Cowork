# Model Cowork for Ollama

The shared dependency-free adapter discovers models from `/api/tags`, routes only to installed model names, and calls `/api/chat` without storing credentials.

```powershell
python .\model_cowork.py discover-ollama
python .\model_cowork.py route backend-api --host ollama --mode local-private
python .\model_cowork.py ollama-chat qwen2.5-coder "Review this handoff..."
```

Default endpoint: `http://127.0.0.1:11434`. Cloud-suffixed Ollama models are excluded from `local-private` mode.

