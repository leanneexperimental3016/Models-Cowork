# Contributing to Model Cowork

Thanks for helping make multi-model coding safer and more useful.

## Good contributions

- Accurate host-installation improvements.
- Routing fixtures that expose a real bad decision or missing fallback.
- Better handoff examples and clearer safety rules.
- Model-registry updates grounded in real availability.
- Small fixes that preserve the dependency-free core.

## Before a pull request

1. Keep changes focused.
2. Add or update a small routing/ledger test when logic changes.
3. Run `python -m unittest discover -s .\core\tests -v`.
4. Do not add API keys, tokens, private paths, or credentials.
5. Explain host-specific assumptions in the pull request.

## Design principles

- Prefer one capable worker over unnecessary orchestration.
- Split only work with disjoint file ownership.
- Preserve honest verification evidence.
- Treat `local-private` as a strict privacy boundary.
- Keep the router dependency-free unless a new dependency has a demonstrated benefit.

