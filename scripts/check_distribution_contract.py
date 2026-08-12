from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def versions() -> dict[str, str]:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    pyproject_match = re.search(r'(?m)^version = "([^"]+)"$', pyproject)
    if pyproject_match is None:
        raise SystemExit("pyproject.toml has no literal project version")
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    codex = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    claude = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    init = (ROOT / "src/tersity_skills/__init__.py").read_text(encoding="utf-8")
    match = re.search(r'^__version__ = "([^"]+)"$', init, re.MULTILINE)
    if match is None:
        raise SystemExit("src/tersity_skills/__init__.py has no literal __version__")
    return {
        "pyproject.toml": pyproject_match.group(1),
        "package.json": package["version"],
        ".codex-plugin/plugin.json": codex["version"],
        ".claude-plugin/plugin.json": claude["version"],
        "src/tersity_skills/__init__.py": match.group(1),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", help="optional release tag, for example v0.1.0")
    args = parser.parse_args()
    discovered = versions()
    expected = next(iter(discovered.values()))
    if any(version != expected for version in discovered.values()):
        raise SystemExit(f"distribution versions differ: {discovered}")
    if args.tag and args.tag != f"v{expected}":
        raise SystemExit(f"tag {args.tag!r} does not match package version v{expected}")
    print(f"distribution contract: {expected} across {len(discovered)} sources")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
