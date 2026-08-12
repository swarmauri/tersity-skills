# Measurement contract

- Treat LOC as physical lines and SLOC as nonblank, non-comment-only source lines.
- Report tool, version, path, exclusions, generated-code policy, and revision with every baseline.
- Compare identical scopes and definitions. Never compare a whole repository with one package.
- Keep tests, generated code, vendored code, examples, and production code as separate cohorts when they matter.
- Treat language-neutral comment detection as an estimate; use a language parser when exact classification is material.
- Do not optimize a repository-wide number by deleting required tests, documentation, observability, validation, types, or public compatibility surfaces.
