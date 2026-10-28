from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import sysconfig
from pathlib import Path

TARGETS = {
    "codex": (Path(".codex/skills"), Path.home() / ".codex/skills"),
    "claude": (Path(".claude/skills"), Path.home() / ".claude/skills"),
    "antigravity": (Path(".agents/skills"), Path.home() / ".gemini/config/skills"),
}


def plugin_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / ".codex-plugin/plugin.json").is_file():
            return parent
        installed_root = parent / "share/tersity-skills/plugin"
        if (installed_root / ".codex-plugin/plugin.json").is_file():
            return installed_root
    return Path(sysconfig.get_path("data")) / "share/tersity-skills/plugin"


def install(target: str, scope: str, project: Path, force: bool) -> int:
    targets = TARGETS if target == "all" else {target: TARGETS[target]}
    for name, (project_dir, user_dir) in targets.items():
        destination = project / project_dir if scope == "project" else user_dir
        destination.mkdir(parents=True, exist_ok=True)
        for skill in (plugin_root() / "skills").iterdir():
            if not (skill / "SKILL.md").is_file():
                continue
            output = destination / skill.name
            if output.exists():
                if not force:
                    raise SystemExit(f"{output} exists; pass --force to replace it")
                shutil.rmtree(output)
            shutil.copytree(skill, output)
            print(f"installed {name}:{skill.name} -> {output}")
    return 0


def scan(arguments: list[str], command: str = "scan") -> int:
    helper = (
        "count-lines/scripts/count_lines.py"
        if command == "count-lines"
        else "measure-codebase/scripts/tersity_scan.py"
    )
    script = plugin_root() / "skills" / helper
    return subprocess.call([sys.executable, str(script), *arguments])


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="tersity-skills")
    commands = root.add_subparsers(dest="command", required=True)
    install_parser = commands.add_parser("install", help="install portable skills")
    install_parser.add_argument("target", choices=[*TARGETS, "all"])
    install_parser.add_argument("--scope", choices=["user", "project"], default="user")
    install_parser.add_argument("--project", type=Path, default=Path.cwd())
    install_parser.add_argument("--force", action="store_true")
    commands.add_parser("path", help="print the bundled plugin root")
    scan_parser = commands.add_parser("scan", help="measure a codebase")
    scan_parser.add_argument("arguments", nargs=argparse.REMAINDER)
    count_parser = commands.add_parser("count-lines", help="count LOC/SLOC with glob filters")
    count_parser.add_argument("arguments", nargs=argparse.REMAINDER)
    return root


def main() -> int:
    # Forward options (including --help) to the actual counting parser.
    if len(sys.argv) > 1 and sys.argv[1] == "count-lines":
        return scan(sys.argv[2:], "count-lines")
    args = parser().parse_args()
    if args.command == "path":
        print(plugin_root())
        return 0
    if args.command == "scan":
        return scan(args.arguments)
    return install(args.target, args.scope, args.project.resolve(), args.force)
