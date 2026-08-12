---
name: debug-terse-code
description: Diagnose and correct defects while avoiding patches, duplicate validation, fallback chains, and compensating code sprawl. Use when debugging failures in compacted or ordinary code, when a fix is growing the codebase, or when asked for a minimal root-cause correction with regression proof.
---

# Debug Terse Code

Correct the owning invariant, not every observed symptom.

## Workflow

1. Reproduce the failure narrowly and capture exact evidence.
2. Map the bad value or state backward to the first violated invariant.
3. Read [references/debugging-rubric.md](references/debugging-rubric.md).
4. Search for authoritative parsing, validation, normalization, state transition, or error translation.
5. Test one falsifiable root-cause hypothesis with inspection or a focused regression.
6. Change the earliest correct owner. Remove redundant downstream guards only with proof.
7. Run the reproducer, focused regression, required gates, and an identical LOC/SLOC comparison.
8. Report cause, correction, proof, size impact, and uncertainty.

Do not add retries, fallbacks, broad exception catches, sentinels, duplicate validation, or environment branches unless the contract requires them. A minimal patch is the smallest semantic correction, not necessarily the fewest changed lines.
