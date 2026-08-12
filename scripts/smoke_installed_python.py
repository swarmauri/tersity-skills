from __future__ import annotations

import tempfile
from pathlib import Path

from tersity_skills import __version__
from tersity_skills.cli import install, plugin_root

SKILLS = {
    "debug-terse-code",
    "evaluate-code-patterns",
    "measure-codebase",
    "tersify-codebase",
}


def main() -> int:
    root = plugin_root()
    assert (root / ".codex-plugin/plugin.json").is_file()
    assert {path.name for path in (root / "skills").iterdir() if path.is_dir()} == SKILLS
    with tempfile.TemporaryDirectory(prefix="tersity-smoke-") as directory:
        project = Path(directory)
        assert install("all", "project", project, False) == 0
        for destination in (".codex/skills", ".claude/skills", ".agents/skills"):
            assert {path.name for path in (project / destination).iterdir()} == SKILLS
    print(f"installed Python distribution {__version__} passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
