<p align="center">
  <img src="https://github.com/swarmauri/swarmauri-sdk/blob/3d4d1cfa949399d7019ae9d8f296afba773dfb7f/assets/swarmauri.brand.theme.svg" alt="Swarmauri" width="480">
</p>

# Tersity Skills

[![CI](https://github.com/swarmauri/tersity-skills/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/swarmauri/tersity-skills/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)

Tersity Skills helps Codex, Claude Code, and Google Antigravity measure a codebase, find opportunities to simplify it, and verify that refactors preserve supported behavior.

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
| `count-lines` | Count LOC/SLOC for paths and globs with include/exclude filters |
| `measure-codebase` | Establish comparable LOC/SLOC and duplication evidence |
| `evaluate-code-patterns` | Rank safe, pattern-based reduction opportunities |
| `tersify-codebase` | Apply reductions with contract and behavior proof |
| `debug-terse-code` | Correct the owning invariant without compensating sprawl |

## Install from source

The repository contains Python and npm package definitions for `tersity-skills`.
Install from a checkout while registry releases are pending.

```bash
git clone https://github.com/swarmauri/tersity-skills.git
cd tersity-skills
```

For Python 3.10 through 3.14, install the CLI with uv:

```bash
uv tool install .
```

For Node.js 20 or newer, install the CLI with npm:

```bash
npm install --global .
```

With the npm installation, `scan` and `count-lines` require Python 3.10 or
newer on `PATH`.

## Install skills into an agent

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

The repository root is also a native Codex and Claude Code plugin. Load the
checkout using your client's local plugin workflow.

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

Count selected files or folders with repeatable include/exclude globs:

```bash
uv run tersity-skills count-lines src tests --include '**/*.py' --exclude '**/generated/**'
uv run tersity-skills count-lines 'src/**/*.py' --format json --output line-counts.json
# Standalone, including after copying only the skill:
uv run skills/count-lines/scripts/count_lines.py . --include '*.py'
```

Counts include per-file LOC, blank, comment-only, and SLOC columns plus totals.
Filters are relative to `--root` (default: current directory); excludes win over
includes. Quote glob patterns. Python uses tokenization; other supported syntaxes
use comment heuristics, and unknown text counts nonblank lines as source.
Skipped binary, undecodable, unreadable, or invalid Python files are reported and
return exit status 1. See the [count-lines skill](skills/count-lines/SKILL.md)
for matching rules and default exclusions.

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

For a first contribution, browse the
[good first issues](https://github.com/swarmauri/tersity-skills/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).

## Distribution contract

PyPI `tersity-skills` and npm `tersity-skills` use the same version and bundle the same `skills/` payload. `scripts/check_distribution_contract.py` verifies the source versions; `scripts/compare_distribution_payloads.py` compares every bundled skill file in the built wheel and npm tarball.

Python packaging, locking, building, smoke testing, and publishing use uv. Node dependency management, testing, and packing use pnpm. The release workflow uses the npm CLI for its final Trusted Publishing upload.
