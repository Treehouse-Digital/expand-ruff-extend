# Expand ruff extend attribute

```
usage: expand-ruff-extend [-h] [-i I] [-o O] [-v]

Expand ruff config's extend attribute and write it out.

options:
  -h, --help    show this help message and exit
  -v            Verbosity (of LOGGER). WARNING by default, -v: INFO, -vv: DEBUG
  -i I          Input config file name (at git repo root)
  -o O          Output config file name (at git repo root)
  --no-ci-skip  Force to still run even on CI

By default, it read's current git repo's root pyproject.toml and writes out
(without comments or previous formatting) to .ruff.toml

This is useful to flatten ruff configs e.g. when "extend" points to a local config
which isn't available on CI/CD. Therefore nothing is done if $CI variable is set to
a non-empty and true-ish value unless --no-ci-skip is explicitly passed in.
```

By default, it read's current git repo's root pyproject.toml and writes out
(without comments or previous formatting) to .ruff.toml

This is used to flatten ruff configs in case "extend" points to a local config
which isn't available on CI/CD.

Also available as a [pre-commit](https://pre-commit.com/#usage) hook:

```yaml
# .pre-commit-config.yaml
repos:
- repo: https://github.com/Treehouse-Digital/expand-ruff-extend
  rev: 0.2.0
  hooks: 
    - id: expand-ruff-extend
```

## Contributing

This repo uses [uv](https://docs.astral.sh/uv/) to perform package managing.

After cloning down the repository:

```bash
uv sync
uv run expand-ruff-extend
```