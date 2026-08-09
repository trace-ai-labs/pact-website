"""Deploy the built site to the gh-pages branch of trace-ai-labs/PACT.

Builds nothing: run `python build.py` first. Copies index.html, paper.pdf, and
.nojekyll into a temporary clone of the gh-pages branch and pushes.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAGES_REPO = "https://github.com/trace-ai-labs/pact.git"
BRANCH = "gh-pages"
FILES = ["index.html", "paper.pdf", ".nojekyll"]


def run(args: list[str], cwd: Path) -> None:
    subprocess.run(args, cwd=cwd, check=True)


def main() -> None:
    for name in FILES:
        if not (HERE / name).exists():
            sys.exit(f"missing {name} - run `python build.py` first")
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / "pages"
        run(["git", "clone", "--branch", BRANCH, "--single-branch", "--depth", "1",
             PAGES_REPO, str(tmp)], cwd=HERE)
        for name in FILES:
            shutil.copy2(HERE / name, tmp / name)
        run(["git", "add", "-A"], cwd=tmp)
        diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=tmp)
        if diff.returncode == 0:
            print("site unchanged - nothing to deploy")
            return
        run(["git", "commit", "-m", "Deploy site"], cwd=tmp)
        run(["git", "push", "origin", BRANCH], cwd=tmp)
    print("deployed to", PAGES_REPO, BRANCH)


if __name__ == "__main__":
    main()
