# Security Policy

## Reporting a vulnerability

Do not open a public issue for a vulnerability involving secrets, data exposure, unsafe routing, or accidental cloud disclosure. Contact the repository owner privately through GitHub and include a clear description, reproduction steps, affected hosts/versions, potential impact, and a safe proof of concept.

## Scope

The main security boundaries are `local-private` routing, secret handling, handoff contents, installer behavior, and unauthorized remote mutations. Model Cowork is an instruction-and-tooling layer; review generated code and provider permissions before production use.

## Secret-protection controls

- `.gitignore` blocks common local credential and certificate files, including `.env`, `*.pem`, `*.key`, `*.p12`, `*.pfx`, `.secrets/`, and cloud-provider credential directories.
- The `Validate` GitHub Actions workflow runs `scripts/scan_secrets.py` on every push and pull request. It scans tracked text files for high-confidence credential signatures without printing the suspected secret value.
- These controls reduce accidental exposure; they do not replace reviewing changes before committing or enabling GitHub's native secret-scanning and push-protection features in the repository settings when available.
