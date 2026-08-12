---
name: measure-codebase
description: Measure LOC, SLOC, language mix, large files, and repeated code blocks in a repository or package. Use before code reduction, refactoring, cleanup, deduplication, complexity reviews, or whenever a trustworthy size baseline and comparable after-measurement are required.
---

# Measure Codebase

Establish evidence before proposing reductions.

## Workflow

1. Inspect repository instructions, status, package boundaries, generated code, and vendored paths.
2. Read [references/measurement-contract.md](references/measurement-contract.md).
3. Run `python scripts/tersity_scan.py <path> --output tersity-baseline.json`. Resolve the script relative to this skill directory.
4. Add `--exclude NAME` for explicit non-product cohorts. Record every exclusion.
5. Inspect largest files and duplicate blocks. Confirm findings against language structure before calling them actionable.
6. Report revision, scope, LOC, SLOC, language mix, generated-code policy, and limitations.
7. Preserve the JSON report until the after-measurement is complete.

Do not equate fewer lines with better code. Measurements rank investigation; behavior, interfaces, and maintainability decide whether a change is good.

## Output contract

Return the baseline revision and exact scope, LOC and SLOC, material cohorts, top evidence-backed candidates, caveats, and exact reproduction command.
