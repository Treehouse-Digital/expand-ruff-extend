"""Git related routines."""

import shutil
import subprocess
from pathlib import Path

__all__ = ("get_repo_root",)


def get_repo_root() -> Path:
    """Fetch path to git repository root based off current working directory."""
    if not (git := shutil.which("git")):
        msg = "No git executable found"
        raise OSError(msg)
    try:
        result = subprocess.run(
            [git, "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=False,
        )
    except subprocess.CalledProcessError as error:
        msg = "Probably not run from a git repository"
        raise OSError(msg) from error
    return Path(result.stdout.strip())
