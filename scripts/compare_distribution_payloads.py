from __future__ import annotations

import argparse
import hashlib
import tarfile
import zipfile
from pathlib import Path

WHEEL_MARKER = "/share/tersity-skills/plugin/skills/"
NPM_MARKER = "package/skills/"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def wheel_skills(path: Path) -> dict[str, str]:
    with zipfile.ZipFile(path) as archive:
        return {
            name.split(WHEEL_MARKER, 1)[1]: digest(archive.read(name))
            for name in archive.namelist()
            if WHEEL_MARKER in name and not name.endswith("/")
        }


def npm_skills(path: Path) -> dict[str, str]:
    with tarfile.open(path, "r:gz") as archive:
        return {
            member.name.removeprefix(NPM_MARKER): digest(archive.extractfile(member).read())
            for member in archive.getmembers()
            if member.isfile() and member.name.startswith(NPM_MARKER)
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("wheel", type=Path)
    parser.add_argument("npm_tarball", type=Path)
    args = parser.parse_args()
    python_payload = wheel_skills(args.wheel)
    npm_payload = npm_skills(args.npm_tarball)
    if not python_payload:
        raise SystemExit("wheel contains no skills")
    if python_payload != npm_payload:
        missing_python = sorted(npm_payload.keys() - python_payload.keys())
        missing_npm = sorted(python_payload.keys() - npm_payload.keys())
        changed = sorted(
            name
            for name in python_payload.keys() & npm_payload.keys()
            if python_payload[name] != npm_payload[name]
        )
        raise SystemExit(
            f"skill payloads differ: only npm={missing_python}, only wheel={missing_npm}, "
            f"changed={changed}"
        )
    print(f"distribution payload: {len(python_payload)} identical skill files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
