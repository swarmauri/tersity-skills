from pathlib import Path

from setuptools import setup

ROOT = Path(__file__).parent
PLUGIN_FILES = [
    (
        str(Path("share/tersity-skills/plugin") / path.relative_to(ROOT).parent),
        [str(path.relative_to(ROOT))],
    )
    for path in ROOT.glob("skills/**/**")
    if path.is_file()
]
PLUGIN_FILES += [
    ("share/tersity-skills/plugin/.codex-plugin", [".codex-plugin/plugin.json"]),
    ("share/tersity-skills/plugin/.claude-plugin", [".claude-plugin/plugin.json"]),
]

setup(data_files=PLUGIN_FILES)
