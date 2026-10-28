#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Count physical LOC and heuristic SLOC in selected text files."""

from __future__ import annotations

import argparse
import fnmatch
import glob
import io
import json
import os
import re
import tokenize
from pathlib import Path

DEFAULT_EXCLUDES = (".git", ".hg", ".svn", ".venv", "node_modules", "__pycache__")
C_STYLE = {
    ".c",
    ".h",
    ".cpp",
    ".hpp",
    ".cs",
    ".go",
    ".java",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".rs",
    ".kt",
    ".swift",
    ".css",
    ".scss",
    ".php",
}
HASH_STYLE = {".sh", ".bash", ".rb", ".yaml", ".yml", ".toml", ".r", ".ps1"}
KEYS = ("loc", "blank", "comments", "sloc")


def matches(path: str, pattern: str) -> bool:
    """Match slash-separated globs; slash-free patterns match any component."""
    pattern = pattern.replace("\\", "/").removeprefix("./").rstrip("/")
    if "/" not in pattern:
        return any(fnmatch.fnmatchcase(part, pattern) for part in path.split("/"))
    parts = pattern.split("/")
    expression = ""
    for index, part in enumerate(parts):
        if part == "**":
            expression += ".*" if index == len(parts) - 1 else "(?:[^/]+/)*"
        else:
            translated = fnmatch.translate(part)
            expression += translated[4:-3]
            if index < len(parts) - 1:
                expression += "/"
    return re.fullmatch(expression, path) is not None


def selected_files(
    root: Path, inputs: list[str], includes: list[str], excludes: list[str]
) -> list[Path]:
    found: set[Path] = set()

    def walk_error(error: OSError) -> None:
        raise error

    def allowed(path: Path) -> bool:
        relative = path.relative_to(root).as_posix()
        return not any(matches(relative, pattern) for pattern in excludes)

    for item in inputs:
        literal = root / item
        candidates = (
            [literal]
            if literal.exists()
            else [Path(value) for value in glob.iglob(str(literal), recursive=True)]
        )
        if not candidates:
            raise ValueError(f"path or glob matched nothing: {item}")
        for candidate in candidates:
            if candidate.is_symlink():
                continue
            candidate = candidate.resolve()
            if not candidate.is_relative_to(root):
                raise ValueError(f"input is outside --root: {item}")
            if not allowed(candidate):
                continue
            if candidate.is_dir():
                for directory, dirs, files in os.walk(
                    candidate, followlinks=False, onerror=walk_error
                ):
                    parent = Path(directory)
                    dirs[:] = [
                        name
                        for name in dirs
                        if not (parent / name).is_symlink() and allowed(parent / name)
                    ]
                    found.update(
                        parent / name
                        for name in files
                        if not (parent / name).is_symlink() and allowed(parent / name)
                    )
            elif candidate.is_file():
                found.add(candidate)
    return sorted(
        path
        for path in found
        if not includes
        or any(matches(path.relative_to(root).as_posix(), pattern) for pattern in includes)
    )


def code_rows(text: str, suffix: str) -> set[int]:
    if suffix == ".py":
        rows: set[int] = set()
        ignored = {
            tokenize.COMMENT,
            tokenize.NL,
            tokenize.NEWLINE,
            tokenize.INDENT,
            tokenize.DEDENT,
            tokenize.ENDMARKER,
            tokenize.ENCODING,
        }
        for token in tokenize.generate_tokens(io.StringIO(text).readline):
            if token.type not in ignored and token.string.strip():
                rows.update(range(token.start[0], token.end[0] + 1))
        return rows
    single = ("//",) if suffix in C_STYLE else ()
    blocks = (("/*", "*/"),) if suffix in C_STYLE else ()
    if suffix in HASH_STYLE:
        single = ("#",)
    if suffix == ".sql":
        single, blocks = ("--",), (("/*", "*/"),)
    if suffix in {".html", ".xml", ".md"}:
        blocks = (("<!--", "-->"),)
    rows = set()
    closing = None
    quote = None
    for number, line in enumerate(text.splitlines(), 1):
        index = 0
        while index < len(line):
            if closing:
                end = line.find(closing, index)
                if end < 0:
                    break
                index, closing = end + len(closing), None
            elif quote:
                rows.add(number)
                if line[index] == "\\":
                    index += 2
                elif line[index] == quote:
                    index, quote = index + 1, None
                else:
                    index += 1
            elif any(line.startswith(marker, index) for marker in single):
                break
            else:
                block = next(
                    ((start, end) for start, end in blocks if line.startswith(start, index)), None
                )
                if block:
                    index, closing = index + len(block[0]), block[1]
                else:
                    if not line[index].isspace():
                        rows.add(number)
                    if line[index] in "\"'`":
                        quote = line[index]
                    index += 1
        if quote != "`":
            quote = None
    return rows


def measure(root: Path, paths: list[Path]) -> dict:
    files, skipped = [], []
    for path in paths:
        relative = path.relative_to(root).as_posix()
        try:
            data = path.read_bytes()
            if b"\0" in data:
                skipped.append({"path": relative, "reason": "binary (NUL byte)"})
                continue
            text = data.decode("utf-8-sig")
            lines = text.splitlines()
            rows = code_rows(text, path.suffix.lower())
        except (OSError, UnicodeError, tokenize.TokenError, IndentationError) as error:
            skipped.append({"path": relative, "reason": str(error)})
            continue
        blank = sum(not line.strip() for line in lines)
        sloc = sum(bool(line.strip()) and number in rows for number, line in enumerate(lines, 1))
        files.append(
            {
                "path": relative,
                "loc": len(lines),
                "blank": blank,
                "comments": len(lines) - blank - sloc,
                "sloc": sloc,
            }
        )
    return {
        "schema_version": 1,
        "root": str(root),
        "definitions": {
            "loc": "physical lines, including a final unterminated line",
            "sloc": "nonblank source lines; Python strings/docstrings count as source; "
            "other supported syntaxes use comment heuristics; unknown text is source",
        },
        "totals": {"files": len(files), **{key: sum(row[key] for row in files) for key in KEYS}},
        "files": files,
        "skipped": skipped,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", default=["."], help="files, folders, or quoted globs")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="base for paths and filters")
    parser.add_argument("--include", "-i", action="append", default=[], metavar="GLOB")
    parser.add_argument("--exclude", "-e", action="append", default=[], metavar="GLOB")
    parser.add_argument("--no-default-excludes", action="store_true")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if not root.is_dir():
        parser.error("--root must be an existing directory")
    excludes = ([] if args.no_default_excludes else list(DEFAULT_EXCLUDES)) + args.exclude
    try:
        paths = selected_files(root, args.paths, args.include, excludes)
    except (ValueError, OSError) as error:
        parser.error(str(error))
    if args.output:
        paths = [path for path in paths if path.resolve() != args.output.resolve()]
    report = measure(root, paths)
    report["selection"] = {"paths": args.paths, "include": args.include, "exclude": excludes}
    if args.format == "json":
        rendered = json.dumps(report, indent=2) + "\n"
    else:
        rendered = "     LOC    Blank Comments     SLOC Path\n"
        for row in [*report["files"], {**report["totals"], "path": "TOTAL"}]:
            rendered += " ".join(f"{row[key]:8d}" for key in KEYS) + f" {row['path']}\n"
        rendered += f"{report['totals']['files']} files; {len(report['skipped'])} skipped\n"
        for row in report["skipped"]:
            rendered += f"Skipped {row['path']}: {row['reason']}\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 1 if report["skipped"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
