#!/usr/bin/env python3
"""Verify that committed static deployment files match the site generator."""

from __future__ import annotations

import difflib
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "src" / "build.py"
GENERATED_DIRS = ("assets",)
GENERATED_ROOT_FILES = ("index.html", "paths.html", "resources.html", "404.html", "azure.html")


def generated_files(directory: Path) -> set[str]:
    files = {
        path.relative_to(directory).as_posix()
        for path in directory.rglob("*")
        if path.is_file()
    }
    return files


def main() -> int:
    if not GENERATOR.is_file():
        print("Missing site generator: src/build.py", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory(prefix="gyaanify-build-") as temp:
        output = Path(temp) / "site"
        subprocess.run(
            [sys.executable, str(GENERATOR), str(output)],
            cwd=ROOT,
            check=True,
        )

        expected = generated_files(output)
        committed = {
            path.relative_to(ROOT).as_posix()
            for path in ROOT.rglob("*")
            if path.is_file()
            and (
                path.name in GENERATED_ROOT_FILES
                or path.parent == ROOT and path.suffix == ".html"
                or path.relative_to(ROOT).parts[0] in GENERATED_DIRS
            )
        }

        missing = sorted(expected - committed)
        stale = sorted(committed - expected)
        mismatched = sorted(
            name for name in expected & committed
            if (output / name).read_bytes() != (ROOT / name).read_bytes()
        )

        if not missing and not stale and not mismatched:
            print(f"Static site is reproducible: {len(expected)} generated files match.")
            return 0

        print("Generated site differs from committed deployment files.", file=sys.stderr)
        if missing:
            print("\nMissing committed files:", file=sys.stderr)
            for name in missing:
                print(f"  + {name}", file=sys.stderr)
        if stale:
            print("\nStale committed files:", file=sys.stderr)
            for name in stale:
                print(f"  - {name}", file=sys.stderr)
        for name in mismatched:
            old = (ROOT / name).read_text(encoding="utf-8", errors="replace").splitlines()
            new = (output / name).read_text(encoding="utf-8", errors="replace").splitlines()
            print(f"\nDiff: {name}", file=sys.stderr)
            for line in list(difflib.unified_diff(
                old, new, fromfile=f"committed/{name}", tofile=f"generated/{name}", lineterm=""
            ))[:80]:
                print(line, file=sys.stderr)
        print("\nRun: python src/build.py .", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
