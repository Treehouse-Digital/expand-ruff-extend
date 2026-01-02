"""Logger and logging routines."""

import logging

from rich.logging import RichHandler
from rich.pretty import pretty_repr

from .constants import CONSOLE

__all__ = ("LOGGER", "log_json")

logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(console=CONSOLE, rich_tracebacks=True)],
)
LOGGER = logging.getLogger("expand-ruff-extend")
LOGGER.setLevel(logging.WARNING)


def log_json(data: object, level: int = logging.DEBUG, name: str | None = None) -> None:
    """Log message for JSON data given, by default to debug."""
    msg = pretty_repr(data, max_width=CONSOLE.width, expand_all=True)
    LOGGER.log(level, f"{name} = {msg}" if name else msg)
