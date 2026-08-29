#!/usr/bin/env python3
"""Dependency-free Model Cowork router and Ollama adapter."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
import urllib.error
import urllib.request

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
REGISTRY = next(
    path for path in (SCRIPT_DIR / "model-registry.json", SCRIPT_DIR.parent / "model-registry.json")
    if path.exists()
)

TASK_CAPABILITIES = {
    "architecture": {"architecture", "reasoning", "review"},
    "frontend-ui": {"frontend", "coding", "vision"},
    "ux-accessibility": {"frontend", "review", "vision"},
    "backend-api": {"backend", "coding", "debugging"},
    "database": {"backend", "coding", "security"},
    "payments-security": {"security", "reasoning", "review"},
    "testing": {"coding", "debugging", "review"},
    "git-github": {"git", "agentic", "review"},
    "documentation": {"docs", "long-context", "review"},
    "mechanical": {"mechanical", "search", "coding"},
}


def load_registry(path: pathlib.Path = REGISTRY) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))["models"]


def ollama_models(base_url: str = "http://127.0.0.1:11434") -> list[str]:
    try:
        with urllib.request.urlopen(f"{base_url.rstrip('/')}/api/tags", timeout=2) as response:
            return [item["name"] for item in json.load(response).get("models", [])]
    except (OSError, KeyError, json.JSONDecodeError, urllib.error.URLError):
        return []


def score(model: dict, wanted: set[str], mode: str) -> int:
    fit = len(wanted.intersection(model.get("capabilities", []))) * 10
    privacy = model.get("privacy", "cloud")
    if mode == "local-private":
        return fit + (40 if privacy == "local" else -1000)
    if mode == "quality":
        return fit + (6 - model.get("cost", 3)) + (5 if model.get("tier") == "reasoning" else 0)
    if mode == "economy":
        return fit + (6 - model.get("cost", 3)) * 4 + model.get("speed", 3)
    return fit + model.get("speed", 3) + (6 - model.get("cost", 3)) * 2


def route(task_type: str, available: set[str], host: str | None, mode: str) -> list[dict]:
    wanted = TASK_CAPABILITIES.get(task_type, {"coding"})
    available = available | {name.removesuffix(":latest") for name in available}
    candidates = []
    for model in load_registry():
        names = {model["id"], *model.get("aliases", [])}
        if available and not names.intersection(available):
            continue
        if host and host not in model.get("hosts", []):
            continue
        rank = score(model, wanted, mode)
        if rank >= 0:
            candidates.append({"model": model["id"], "score": rank, "matched": sorted(wanted.intersection(model.get("capabilities", [])))})
    return sorted(candidates, key=lambda item: (-item["score"], item["model"]))


def assert_no_file_conflicts(ledger: dict) -> None:
    owners: dict[str, str] = {}
    for assignment in ledger.get("assignments", []):
        if assignment.get("status") not in {"planned", "active", "handoff"}:
            continue
        for file_name in assignment.get("files", []):
            normalized = file_name.replace("\\", "/").lower()
            if normalized in owners and owners[normalized] != assignment["id"]:
                raise ValueError(f"file ownership conflict: {file_name} ({owners[normalized]} and {assignment['id']})")
            owners[normalized] = assignment["id"]


def ollama_chat(model: str, prompt: str, base_url: str = "http://127.0.0.1:11434") -> str:
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}], "stream": False}).encode()
    request = urllib.request.Request(f"{base_url.rstrip('/')}/api/chat", body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=300) as response:
        return json.load(response)["message"]["content"]


def main() -> int:
    parser = argparse.ArgumentParser(prog="model-cowork")
    sub = parser.add_subparsers(dest="command", required=True)
    discover = sub.add_parser("discover-ollama")
    discover.add_argument("--url", default="http://127.0.0.1:11434")
    routing = sub.add_parser("route")
    routing.add_argument("task_type", choices=sorted(TASK_CAPABILITIES))
    routing.add_argument("--host", choices=["codex", "claude", "copilot", "antigravity", "ollama"])
    routing.add_argument("--mode", choices=["balanced", "quality", "economy", "local-private"], default="balanced")
    routing.add_argument("--available", nargs="*", default=[])
    check = sub.add_parser("check-ledger")
    check.add_argument("path", type=pathlib.Path)
    chat = sub.add_parser("ollama-chat")
    chat.add_argument("model")
    chat.add_argument("prompt")
    chat.add_argument("--url", default="http://127.0.0.1:11434")
    args = parser.parse_args()

    if args.command == "discover-ollama":
        print(json.dumps(ollama_models(args.url), indent=2)); return 0
    if args.command == "route":
        available = set(args.available)
        if args.host == "ollama" and not available:
            available = set(ollama_models())
        print(json.dumps(route(args.task_type, available, args.host, args.mode)[:5], indent=2)); return 0
    if args.command == "check-ledger":
        assert_no_file_conflicts(json.loads(args.path.read_text(encoding="utf-8")))
        print("ledger ok"); return 0
    if args.command == "ollama-chat":
        print(ollama_chat(args.model, args.prompt, args.url)); return 0
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, urllib.error.URLError) as error:
        print(f"model-cowork: {error}", file=sys.stderr)
        raise SystemExit(1)
