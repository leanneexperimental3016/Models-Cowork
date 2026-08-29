#!/usr/bin/env python3
"""Fail CI when a tracked file contains a high-confidence credential signature.

The scanner deliberately reports only the file, line, and signature category;
it never echoes a possible secret into CI logs.
"""

from __future__ import annotations

import pathlib
import re
import subprocess
import sys


REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parent.parent

PATTERNS = {
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b|\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    "OpenAI API key": re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
    "AWS access key": re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    "Google API key": re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    "Private key": re.compile(r"-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----"),
}


def tracked_files() -> list[pathlib.Path]:
    result = subprocess.run(
        ["git", "-C", str(REPOSITORY_ROOT), "ls-files", "-z"],
        check=True,
        capture_output=True,
    )
    return [pathlib.Path(value.decode()) for value in result.stdout.split(b"\0") if value]


def main() -> int:
    findings: list[tuple[pathlib.Path, int, str]] = []
    for path in tracked_files():
        try:
            text = (REPOSITORY_ROOT / path).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            for category, pattern in PATTERNS.items():
                if pattern.search(line):
                    findings.append((path, line_number, category))
    if not findings:
        print("Secret scan passed: no high-confidence credential signatures found.")
        return 0
    print("Secret scan failed. Remove or rotate the credential before committing:", file=sys.stderr)
    for path, line_number, category in findings:
        print(f"- {path}:{line_number} ({category})", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
