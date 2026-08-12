<p align="center">
  <img src="https://github.com/swarmauri/swarmauri-sdk/blob/3d4d1cfa949399d7019ae9d8f296afba773dfb7f/assets/swarmauri.brand.theme.svg" alt="Swarmauri" width="480">
</p>

# Tersity Skills

[![PyPI](https://img.shields.io/pypi/v/tersity-skills)](https://pypi.org/project/tersity-skills/)
[![Python](https://img.shields.io/pypi/pyversions/tersity-skills)](https://pypi.org/project/tersity-skills/)
[![npm](https://img.shields.io/npm/v/tersity-skills)](https://www.npmjs.com/package/tersity-skills)
[![Downloads](https://img.shields.io/pypi/dm/tersity-skills)](https://pypi.org/project/tersity-skills/)
[![Hits](https://hits.sh/github.com/swarmauri/tersity-skills.svg)](https://hits.sh/github.com/swarmauri/tersity-skills/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)

Portable Codex, Claude Code, and Google Antigravity skills for making a codebase smaller without changing its supported behavior.

## Features

- Reproducible physical LOC and heuristic SLOC baselines
- Language mix, largest-file, generated-file, and repeated-block evidence
- Pattern-led reduction recommendations with confidence and risk
- Safe deletion, deduplication, consolidation, and simplification workflows
- Root-cause debugging that resists fallback and validation sprawl
- One platform-agnostic `skills/` source shared by every supported agent
- Dependency-free scanner; Python and npm packages install identical skill content

## Skills

| Skill | Purpose |
| --- | --- |
| `measure-codebase` | Establish comparable LOC/SLOC and duplication evidence |
| `evaluate-code-patterns` | Rank safe, pattern-based reduction opportunities |
| `tersify-codebase` | Apply reductions with contract and behavior proof |
| `debug-terse-code` | Correct the owning invariant without compensating sprawl |

## Install

Python 3.10 through 3.14:

```bash
uv tool install tersity-skills
# or
pipx install tersity-skills
```

Node.js 20 or newer:

```bash
pnpm add --global tersity-skills
# npm consumers can also use: npm install --global tersity-skills
```

Install skills for a user:

```bash
tersity-skills install codex
tersity-skills install claude
tersity-skills install antigravity
# or all three
tersity-skills install all
```

Install into the current project instead:

```bash
tersity-skills install all --scope project
```

Project destinations are `.codex/skills`, `.claude/skills`, and `.agents/skills`. User destinations are `~/.codex/skills`, `~/.claude/skills`, and `~/.gemini/config/skills`.

The repository root is also a native Codex and Claude plugin. During development, load it from its checkout using the client's local-plugin workflow.

## Usage

Ask the agent to:

```text
Measure this package, identify the safest high-value reductions, implement them,
and prove behavior is unchanged.
```

Run the deterministic scanner directly:

```bash
tersity-skills scan . --output tersity-baseline.json
```

The report states its LOC and SLOC definitions. Treat duplicate blocks as investigation leads: language-aware inspection and tests must confirm ownership and semantics.

## Optimization contract

Tersity means less accidental code, not fewer lines at any cost. The skills reject minification, deletion of tests or safeguards, opaque metaprogramming, premature abstractions, and metric-only rewrites. A successful reduction preserves explicit invariants, passes repository gates, and compares the same measurement scope before and after.

## Development

```bash
uv sync --locked
uv run --frozen ruff check .
uv run --frozen pytest
uv build --no-sources
pnpm install --frozen-lockfile
pnpm run check
pnpm run pack:check
```

## Distribution contract

PyPI `tersity-skills` and npm `tersity-skills` use the same version and bundle the same `skills/` payload. `scripts/check_distribution_contract.py` verifies the source versions; `scripts/compare_distribution_payloads.py` compares every bundled skill file in the built wheel and npm tarball.

Python packaging, locking, building, smoke testing, and publishing use uv. Node dependency management, testing, and packing use pnpm. The release workflow uses the npm CLI only for the final npm Trusted Publishing upload because npm's OIDC exchange is implemented by that CLI. Because this repository is private, npm provenance attestations are not available.
