# toolz-stubs

[![CI](https://github.com/mgrinshpon/toolz-stubs/actions/workflows/ci.yml/badge.svg)](https://github.com/mgrinshpon/toolz-stubs/actions/workflows/ci.yml)

Type stubs for [toolz](https://github.com/pytoolz/toolz) and [tlz](https://github.com/pytoolz/toolz/tree/main/tlz) - Python functional programming libraries.

Type hinting for [cytoolz](https://github.com/pytoolz/cytoolz) is available via [tlz](https://github.com/pytoolz/toolz/tree/main/tlz).

## Installation

```bash
pip install toolz-stubs
```

This installs type stubs for both `toolz` and `tlz`.

## Usage

Once installed, type checkers like mypy, pyright, or basedpyright will automatically use these stubs:

```python
import toolz
from toolz import curry, compose, pipe

@curry
def add(x: int, y: int) -> int:
    return x + y

# Type checkers will understand these operations
add_five = add(5)  # Correctly typed as partial function
result = add_five(3)  # Type checked as int
```

The same types work with `tlz`:

```python
import tlz
from tlz import curry, compose, pipe

# Identical API, same type hints
result = tlz.pipe(data, transform1, transform2)
```

## What's Included

This package provides type stubs (`.pyi` files) for:

- **toolz**: The pure Python functional programming library
- **tlz**: The auto-selecting wrapper that uses cytoolz (if available) or falls back to toolz

Modules covered:
- `toolz.functoolz` / `tlz.functoolz` - Function manipulation (curry, compose, pipe, etc.)
- `toolz.itertoolz` / `tlz.itertoolz` - Iterator utilities (groupby, partition, sliding_window, etc.)
- `toolz.dicttoolz` / `tlz.dicttoolz` - Dictionary operations (merge, valmap, keyfilter, etc.)
- `toolz.curried` / `tlz.curried` - Pre-curried versions of all functions
- `toolz.recipes` / `tlz.recipes` - Common recipes (countby, partitionby)
- `toolz.sandbox` / `tlz.sandbox` - Experimental utilities

## Development

```bash
# Install dependencies
uv sync

# Run type checker
uv run basedpyright

# Run tests
uv run pytest

# Build
uv build
```

## Contributing

Contributions are welcome! Areas that could use improvement:

1. More precise generic types
2. Additional overloads for functions with variable signatures
3. Improved curry and composition typing
4. Protocol types for duck-typed parameters

## License

BSD 3-Clause (same as toolz)
