---
name: evaluate-code-patterns
description: Evaluate a code project for duplication, repeated control flow, needless wrappers, dead code, over-abstraction, configuration sprawl, and other pattern-based reduction opportunities. Use when asked to review, recommend, prioritize, compact, sanitize, clean up, or find why a package contains more code than its behavior requires.
---

# Evaluate Code Patterns

Find accidental repetition without rewarding clever compression.

## Workflow

1. Map package, public API, runtime, test, generated, and compatibility boundaries.
2. Invoke or follow `measure-codebase` for a reproducible baseline.
3. Read [references/pattern-catalog.md](references/pattern-catalog.md).
4. Use language-aware search, references, tests, and static tooling to confirm each candidate. Scanner output is a lead, not proof.
5. Group candidates by shared cause and rank by removable SLOC, confidence, behavior risk, API risk, and verification cost.
6. Recommend the smallest coherent change set with explicit acceptance gates.

Preserve public behavior. Never count deleting tests, types, validation, accessibility, security checks, or diagnostics as optimization. Do not create a generic abstraction until multiple real consumers share one stable policy.

## Output contract

For every recommendation, give locations, repeated pattern, estimated reduction, semantic invariant, confidence, risk, and proof command. Separate measured fact, inference, and proposal.
