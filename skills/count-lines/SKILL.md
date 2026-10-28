---
name: count-lines
description: Count physical LOC and source lines (SLOC) for files, folders, or glob selections with include and exclude filters. Use for scoped line counts and reproducible size comparisons; use measure-codebase for duplication and broader reduction evidence.
---

# Count Lines

Run the self-contained helper relative to this skill directory:

```bash
uv run /path/to/count-lines/scripts/count_lines.py --root /path/to/repo src tests --include '**/*.py' --exclude '**/generated/**'
```

The installed package exposes the same helper as `tersity-skills count-lines`.
From the package checkout, use `uv run tersity-skills count-lines ...`.
The helper needs Python 3.10+ and no dependencies; `python count_lines.py ...`
also works when uv is unavailable.

Examples (quote globs so the tool receives them unchanged):

```bash
tersity-skills count-lines src/main.py
tersity-skills count-lines 'src/**/*.py' 'tests/**/*.py' --exclude '*_generated.py'
tersity-skills count-lines . --include '**/*.ts' --include '**/*.tsx' --exclude 'src/vendor/**' --format json --output line-counts.json
```

Paths and positional globs resolve against `--root` (the current directory by
default); folders recurse and overlapping selections count each file once.
Filters use root-relative paths with `/` separators and case-sensitive matching:
`*`, `?`, and character classes match within a component; `**` matches zero or
more directories. A pattern without `/` matches any path component, so
`--exclude generated` excludes that directory anywhere. Repeated includes form
a union; excludes always win. An unmatched positional path/glob is an error;
filters selecting no files produce zero totals.

By default `.git`, `.hg`, `.svn`, `.venv`, `node_modules`, and `__pycache__` are
excluded. Use `--no-default-excludes` to override. Git ignore files are not read.
Inputs must stay within `--root`; symlink entries are skipped. A report output
file is excluded from its own measurement.

LOC counts physical lines, including an unterminated final line. Each line is
blank, comment-only, or SLOC; lines containing code and comments count as SLOC.
Python uses tokenization and counts strings/docstrings as source. Common C-style,
hash-comment, SQL, HTML/XML, and Markdown syntaxes use heuristics. Unknown UTF-8
text counts all nonblank lines as source. These are physical source counts,
not logical statements or a full language-parser analysis; embedded languages,
raw strings, heredocs, and nested comments can affect heuristic accuracy.

Binary (NUL-containing), non-UTF-8, unreadable, or untokenizable Python files
are reported under `skipped`; exit status 1 signals an incomplete count.
Invalid selections/options exit 2. Successful counts exit 0.

Report totals, material skips, exact command, and SLOC limitations. For before/
after comparisons preserve the same root, selections, filters, and tool version.
