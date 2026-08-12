import json
import subprocess
import sys
from pathlib import Path

SCANNER = Path("skills/measure-codebase/scripts/tersity_scan.py")


def test_scanner_counts_and_finds_duplicate_blocks(tmp_path: Path) -> None:
    block = "\n".join(f"value_{index} = {index}" for index in range(8))
    (tmp_path / "a.py").write_text(f"# comment\n\n{block}\n", encoding="utf-8")
    (tmp_path / "b.py").write_text(f"{block}\n", encoding="utf-8")
    output = subprocess.run(
        [sys.executable, str(SCANNER), str(tmp_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    report = json.loads(output.stdout)
    assert report["totals"] == {
        "files": 2,
        "loc": 18,
        "blank": 1,
        "comments": 1,
        "sloc": 16,
    }
    assert report["languages"]["Python"]["files"] == 2
    assert report["duplicate_blocks"][0]["estimated_excess_sloc"] >= 8


def test_scanner_excludes_named_directory(tmp_path: Path) -> None:
    included = tmp_path / "src"
    excluded = tmp_path / "generated"
    included.mkdir()
    excluded.mkdir()
    (included / "kept.py").write_text("kept = True\n", encoding="utf-8")
    (excluded / "skip.py").write_text("skip = True\n", encoding="utf-8")
    output = subprocess.run(
        [sys.executable, str(SCANNER), str(tmp_path), "--exclude", "generated"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert json.loads(output.stdout)["totals"]["files"] == 1
