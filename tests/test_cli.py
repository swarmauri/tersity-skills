from pathlib import Path

from tersity_skills.cli import install, plugin_root


def test_source_plugin_root() -> None:
    assert (plugin_root() / ".codex-plugin/plugin.json").is_file()


def test_project_install_copies_all_skills(tmp_path: Path) -> None:
    assert install("codex", "project", tmp_path, False) == 0
    installed = tmp_path / ".codex/skills"
    assert {path.name for path in installed.iterdir()} == {
        "debug-terse-code",
        "evaluate-code-patterns",
        "measure-codebase",
        "tersify-codebase",
    }
