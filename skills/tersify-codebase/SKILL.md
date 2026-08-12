---
name: tersify-codebase
description: Implement safe codebase reduction through deletion, deduplication, simplification, consolidation, pattern replacement, and cleanup while preserving behavior and public contracts. Use when asked to make code terse, reduce LOC or SLOC, refactor duplication, compact a package, sanitize implementation sprawl, or apply evaluated reduction recommendations.
---

# Tersify Codebase

Reduce the code required to express the same supported behavior.

## Workflow

1. Read repository instructions and inspect dirty state. Preserve unrelated changes.
2. Establish a baseline with `measure-codebase` and rank candidates with `evaluate-code-patterns`.
3. Read [references/change-protocol.md](references/change-protocol.md).
4. Freeze public API, outputs, side effects, errors, persistence, concurrency, performance budgets, and supported versions.
5. Add characterization tests only where proof is insufficient.
6. Apply one coherent reduction at a time. Prefer deletion or one authority over a new layer.
7. Run focused checks after each change and repository-required gates at the end.
8. Re-run the identical measurement command and review the diff manually.
9. Report gross removed, gross added, net LOC/SLOC change, behavior proof, and residual risks separately.

Stop when reduction would break a contract, weaken safety, merge distinct concepts, obscure flow, or increase operational risk. Never minify source or introduce dynamic behavior for line-count optics.
