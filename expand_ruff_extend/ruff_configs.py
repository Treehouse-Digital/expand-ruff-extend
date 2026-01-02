"""Routines to process ruff configurations."""

import os
from collections import ChainMap
from pathlib import Path
from string import Template

import toml_rs  # I/O, fast and compatible with TOML v1.0 and v1.1

from .logger import LOGGER, log_json

__all__ = ("deep_merged", "expanded_contents", "ruff_contents")


def ruff_contents(toml_path: Path) -> dict:
    """Fetch ruff settings from given TOML file path."""
    results = {}
    if toml_path.is_file():
        LOGGER.info(f"Reading: {toml_path}")
        contents: dict = toml_rs.loads(toml_path.read_text())
        results: dict = (
            contents.get("tool", {}).get("ruff", {})
            if toml_path.name == "pyproject.toml"
            else contents
        )
    return results


def deep_merged(base: dict, updates: dict) -> dict:
    """Apply updates onto base dict, recursively merging sub-dicts."""
    return {
        key: (
            deep_merged(base_dict, updates_dict)
            if isinstance(base_dict := base.get(key), dict)
            and isinstance(updates_dict := updates.get(key), dict)
            else value
        )
        for key, value in dict(ChainMap(updates, base)).items()
    }


def expanded_contents(in_toml: Path) -> str:
    """Expand and dump config string that will be read from given path.

    If no "extend" property is found, then empty string is returned (no expansion
    took place).
    """
    heading = f"# Auto-generated from expanding out {in_toml.name}"
    config: dict = ruff_contents(in_toml)
    log_json(config, name="(base) config")
    if extend := config.pop("extend", None):
        extend_path = Path(Template(extend).substitute(os.environ))
        config: dict = deep_merged(ruff_contents(extend_path), config)
        log_json(config, name="(merged) config")
    else:
        LOGGER.warning("No extend property found")
    return "" if extend is None or not config else f"{heading}\n{toml_rs.dumps(config)}"
