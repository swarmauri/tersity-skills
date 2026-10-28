import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path("skills/count-lines/scripts/count_lines.py").resolve()


def run(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(root), *args, "--format", "json"],
        capture_output=True,
        text=True,
    )


def test_files_globs_filters_and_overlaps(tmp_path: Path) -> None:
    for name in ["src/a.py", "src/nested/b.py", "src/generated/c.py", "src/a.js"]:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("x = 1\n", encoding="utf-8")
    result = run(
        tmp_path,
        "src",
        "src/**/*.py",
        "src/a.py",
        "--include",
        "**/*.py",
        "--exclude",
        "src/generated/**",
    )
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert [row["path"] for row in report["files"]] == ["src/a.py", "src/nested/b.py"]
    assert report["totals"]["sloc"] == 2


def test_comment_counts_and_line_endings(tmp_path: Path) -> None:
    (tmp_path / "a.py").write_bytes(b'# comment\r\n\r\nx = "# source"\r\n"""doc\r\ntext"""')
    (tmp_path / "b.js").write_text('/* comment\nend */ x(); // code\n"//";\n', encoding="utf-8")
    result = run(tmp_path)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["totals"] == {
        "files": 2,
        "loc": 8,
        "blank": 1,
        "comments": 2,
        "sloc": 5,
    }


def test_defaults_repeated_includes_and_empty_files(tmp_path: Path) -> None:
    (tmp_path / ".venv").mkdir()
    (tmp_path / ".venv/a.py").write_text("x = 1\n", encoding="utf-8")
    (tmp_path / "empty.txt").touch()
    result = run(tmp_path, "--include", "*.txt", "--include", "*.py")
    assert json.loads(result.stdout)["totals"]["files"] == 1
    result = run(tmp_path, "--no-default-excludes")
    assert json.loads(result.stdout)["totals"]["files"] == 2
    assert json.loads(run(tmp_path, "--include", "*.rs").stdout)["totals"]["files"] == 0


def test_incomplete_counts_and_invalid_selection(tmp_path: Path) -> None:
    (tmp_path / "binary.py").write_bytes(b"\0")
    (tmp_path / "encoding.txt").write_bytes(b"\xff")
    (tmp_path / "invalid.py").write_text('"""unclosed', encoding="utf-8")
    result = run(tmp_path)
    assert result.returncode == 1
    assert len(json.loads(result.stdout)["skipped"]) == 3
    assert run(tmp_path, "missing*.py").returncode == 2
    assert run(tmp_path, "..").returncode == 2


def test_output_not_counted(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("hello\n", encoding="utf-8")
    output = tmp_path / "report.json"
    output.write_text("previous report\n", encoding="utf-8")
    result = run(tmp_path, "--output", str(output))
    assert result.returncode == 0, result.stderr
    assert json.loads(output.read_text(encoding="utf-8"))["totals"]["files"] == 1


def test_package_command_forwards_leading_options() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from tersity_skills.cli import main; main()",
            "count-lines",
            "--include",
            "*.py",
            "src",
            "--format",
            "json",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["totals"]["files"] >= 2
