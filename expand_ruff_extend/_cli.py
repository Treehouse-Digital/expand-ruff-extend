#!/bin/env python3
"""Expand ruff config's extend attribute and write it out.

By default, it read's current git repo's root pyproject.toml and writes out
(without comments or previous formatting) to .ruff.toml

This is useful to flatten ruff configs e.g. when "extend" points to a local config
which isn't available on CI/CD. Therefore nothing is done if $CI variable is set to
a non-empty and true-ish value unless --no-ci-skip is explicitly passed in.
"""

import argparse
import logging
import os
from collections.abc import Sequence
from pathlib import Path

from .constants import DEFAULT_IN, DEFAULT_OUT
from .git import get_repo_root
from .logger import LOGGER
from .ruff_configs import expanded_contents


def on_ci() -> bool:
    """Whether we're on CI."""
    lower_true_values = ("true", "t", "1", "yes", "y", "on")
    return (value := os.getenv("CI")) and value.lower() in lower_true_values


def main(argv: Sequence[str] | None = None) -> None:
    """Parse arguments and read/write out ruff configurations."""
    module_docstrings = str(__doc__)  # Ensure at least 1 empty line in there!
    description, epilog = module_docstrings.split("\n\n", 1)
    parser = argparse.ArgumentParser(
        Path(__file__).name,
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    v_help = "Verbosity (of LOGGER). WARNING by default, -v: INFO, -vv: DEBUG"
    parser.add_argument("-v", help=v_help, action="count", default=0)
    config_suffix = " config file name (at git repo root)"
    parser.add_argument("-i", help=f"Input {config_suffix}", default=DEFAULT_IN)
    parser.add_argument("-o", help=f"Output {config_suffix}", default=DEFAULT_OUT)
    parser.add_argument(
        "--no-ci-skip", action="store_true", help="Force to still run even on CI"
    )

    args = parser.parse_args(argv)
    LOGGER.setLevel([logging.WARNING, logging.INFO, logging.DEBUG][args.v])
    if on_ci() and not args.no_ci_skip:
        LOGGER.info("Skipping as we're on CI and --no-ci-skip not passed in")
    else:
        repo_root = get_repo_root()
        if out_text := expanded_contents(repo_root / args.i):
            out_toml = repo_root / args.o
            out_toml.write_text(out_text)
            LOGGER.info(f"Written expanded to: {out_toml}")
        else:
            LOGGER.warning("No expanded ruff configs to write")


if __name__ == "__main__":
    main()
