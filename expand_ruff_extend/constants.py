"""Constants used throughout this package."""

from rich.console import Console

__all__ = ("CONSOLE", "DEFAULT_IN", "DEFAULT_OUT")

CONSOLE = Console()
"""Common console used throughout this script."""

DEFAULT_IN = "pyproject.toml"
"""Filename at base of git repo to find ruff configs from."""

DEFAULT_OUT = ".ruff.toml"
"""Filename at base of git repo to write out expanded configs from."""
