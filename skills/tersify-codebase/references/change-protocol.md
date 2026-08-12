# Safe reduction protocol

## Acceptance gates

1. Same scoped inputs produce the same supported outputs and side effects.
2. Public imports, symbols, routes, schemas, files, and commands remain compatible unless explicitly changed.
3. Focused regression tests and repository-required checks pass independently.
4. The after-measurement uses the baseline's exact tool, scope, exclusions, and generated-code policy.
5. Complexity is not hidden in configuration, reflection, generated artifacts, or dependencies.
6. New abstractions have multiple concrete consumers and describe stable policy.

## Change order

1. Remove unreachable or obsolete code with evidence.
2. Use an existing canonical implementation.
3. Replace repeated mechanics with data or standard language features.
4. Extract a small local function.
5. Introduce a shared abstraction only after the common contract is proven.
