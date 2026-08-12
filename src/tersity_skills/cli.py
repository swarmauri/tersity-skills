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
    source_root = Path(__file__).resolve().parents[2]
    if (source_root / ".codex-plugin/plugin.json").is_file():
        return source_root
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


def scan(arguments: list[str]) -> int:
    script = plugin_root() / "skills/measure-codebase/scripts/tersity_scan.py"
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
    return root


def main() -> int:
    args = parser().parse_args()
    if args.command == "path":
        print(plugin_root())
        return 0
    if args.command == "scan":
        return scan(args.arguments)
    return install(args.target, args.scope, args.project.resolve(), args.force)
