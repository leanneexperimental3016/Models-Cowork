# Security Policy

## Reporting a vulnerability

Do not open a public issue for a vulnerability involving secrets, data exposure, unsafe routing, or accidental cloud disclosure. Contact the repository owner privately through GitHub and include a clear description, reproduction steps, affected hosts/versions, potential impact, and a safe proof of concept.

## Scope

The main security boundaries are `local-private` routing, secret handling, handoff contents, installer behavior, and unauthorized remote mutations. Model Cowork is an instruction-and-tooling layer; review generated code and provider permissions before production use.

