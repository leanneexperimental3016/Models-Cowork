---
name: model-cowork
description: Route, divide, hand off, review, and integrate software work across specialist models and coding apps. Use for app, website, API, repository, debugging, UI/UX, payments, testing, GitHub, or multi-model coding tasks.
---

# Model Cowork

Coordinate only when coordination reduces work. Keep a single owner for small or tightly coupled changes.

## Workflow

1. Inspect the repository, instructions, current changes, runtime, and available tools/models. Never guess availability from the registry.
2. Classify work as architecture, frontend-ui, ux-accessibility, backend-api, database, payments-security, testing, git-github, documentation, language-stack, or mechanical.
3. Choose `balanced` unless the user requests `quality`, `economy`, or `local-private`. In local-private mode, do not send code or context to cloud models.
4. Split only independent work. Each active assignment must own a disjoint file set in `.model-cowork/ledger.json`. Reject overlaps before delegation.
5. Prefer native subagents/model controls. If the target is unavailable or external, emit the handoff packet from `templates/HANDOFF.md` instead of claiming delegation occurred.
6. Require each worker to return changed files, concise rationale, exact checks run and results, and unresolved risks. A failed or skipped check is evidence, not success.
7. The lead integrates in ledger order, rechecks diffs and conflicts, runs the smallest relevant test set, then broader checks proportional to risk.
8. Only the integrator may commit or push. Push, deploy, payment changes, secrets, and destructive operations require explicit user authorization.

## Routing

Score only models actually available in the host. Use task-fit first, then mode:

- `balanced`: fit, latency, relative token cost, privacy, and tools.
- `quality`: reasoning/review strength before speed or cost.
- `economy`: deterministic tools, local models, and fast models before escalation.
- `local-private`: models marked `privacy: local` only; fail closed when none are available.

Run `model_cowork.py route <task-type> --host <host> --mode <mode> --available <models...>` when Python is available. Otherwise apply the same rules directly from `model-registry.json`.

Use strong reasoning for architecture, difficult debugging, security, payment boundaries, and final review. Use coding specialists for implementation. Use vision-capable models for screenshot/UI work. Use fast models for search, formatting, documentation, and bounded mechanical edits. Use local Ollama models for private or inexpensive tasks and escalate only when permitted and verification fails.

## Specialists

- **Lead/integrator:** scopes, assigns ownership, resolves conflicts, verifies, and alone commits/pushes.
- **Architecture:** interfaces, boundaries, migrations, and high-impact tradeoffs.
- **Frontend UI:** components, styling, responsive behavior, performance, and visual fidelity.
- **UX/accessibility:** journeys, interaction states, semantics, keyboard use, and assistive technology.
- **Backend/API:** contracts, authentication, integrations, errors, and concurrency.
- **Language/stack:** framework and language-specific implementation with repository-native patterns.
- **Database:** schemas, migrations, transactions, locking, integrity, and rollback.
- **Payments/security:** trust boundaries, money precision, idempotency, secrets, threat review, and safe failure.
- **Testing:** focused regression checks, integration tests, static checks, and honest evidence.
- **Git/GitHub:** branches, diffs, PRs, reviews, CI, pull/push; no remote mutation without authorization.
- **Documentation:** precise user/developer documentation grounded in verified behavior.
- **Mechanical:** search, formatting, renames, inventory, and other low-risk bounded work.

## Context and token discipline

- Give workers only their objective, owned files, required interfaces, constraints, and relevant evidence.
- Reference files instead of pasting entire repositories. Summarize discovery once and reuse it.
- Use deterministic search, parsers, formatters, and tests before model calls.
- Stop delegating when coordination cost exceeds the remaining work.
- Never hide verification failures to save tokens.

## Handoff

Return both a readable summary and valid JSON matching `handoff.schema.json`. Required fields: objective, assigned files, constraints, completed work, verification, risks, and expected return. Preserve an explicit `token_budget` only when the user provided one.

## Completion gate

Before completion: confirm no active ownership conflicts; inspect all returned diffs; run relevant checks; record skipped checks and why; confirm no unauthorized push/deploy/payment/destructive action; and leave the ledger in `verified`, `integrated`, or honestly `blocked` states.
