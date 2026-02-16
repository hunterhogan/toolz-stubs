# toolz-stubs

[![CI](https://github.com/mgrinshpon/toolz-stubs/actions/workflows/ci.yml/badge.svg)](https://github.com/mgrinshpon/toolz-stubs/actions/workflows/ci.yml)
[![basedpyright](https://img.shields.io/endpoint?url=https://docs.basedpyright.com/latest/badge.json)](https://docs.basedpyright.com)
[![pyright](https://img.shields.io/badge/type--checked-pyright-blue)](https://github.com/microsoft/pyright)

Type stubs for [toolz](https://github.com/pytoolz/toolz) and [tlz](https://github.com/pytoolz/toolz/tree/master/tlz) - Python functional programming libraries.

## Installation

```bash
pip install toolz-stubs
```

This installs type stubs for both `toolz` and `tlz`.

## Usage

Once installed, type checkers like mypy, pyright, or basedpyright will automatically use these stubs:

```python
import toolz

bills = {"Alice": [20, 15, 30], "Bob": [10, 35]}
totals = toolz.valmap(sum, bills)  # dict[str, int]

even_entries = toolz.keyfilter(lambda k: k % 2 == 0, {1: "a", 2: "b", 3: "c"})  # dict[int, str]

names = ["Alice", "Bob", "Charlie", "Anna"]
grouped = toolz.groupby(lambda s: s[0], names)  # dict[str, list[str]]
```

### Using with cytoolz

When you `pip install toolz`, you also get a second package called [`tlz`](https://github.com/pytoolz/toolz/tree/master/tlz). It's a thin auto-selecting wrapper: if [cytoolz](https://github.com/pytoolz/cytoolz) (the C-accelerated version) is installed, `tlz` imports from it; otherwise it falls back to pure-Python `toolz`. The API is identical either way.

If you use `cytoolz`, you can switch your imports to `tlz` to get the same performance with type checking support and a graceful fallback:

```python
# before
from cytoolz.dicttoolz import merge, valmap
from cytoolz.functoolz import curry, compose, pipe

# after — same performance, now with type stubs
from tlz.dicttoolz import merge, valmap
from tlz.functoolz import curry, compose, pipe
```

## What's Included

This package provides type stubs (`.pyi` files) for:

- **toolz**: The pure Python functional programming library
- **tlz**: The auto-selecting wrapper (uses cytoolz if installed, otherwise falls back to toolz)

Modules covered:
- `toolz.functoolz` / `tlz.functoolz` - Function manipulation (curry, compose, pipe, etc.)
- `toolz.itertoolz` / `tlz.itertoolz` - Iterator utilities (groupby, partition, sliding_window, etc.)
- `toolz.dicttoolz` / `tlz.dicttoolz` - Dictionary operations (merge, valmap, keyfilter, etc.)
- `toolz.curried` / `tlz.curried` - Pre-curried versions of all functions
- `toolz.recipes` / `tlz.recipes` - Common recipes (countby, partitionby)
- `toolz.sandbox` / `tlz.sandbox` - Experimental utilities

## Development

```bash
make sync    # Install dependencies
make check   # Run type checker
make test    # Run tests
make lint    # Run linter
make format  # Check formatting
make build   # Build wheel
```

If manually running commands, be sure to specify `--no-editable` or hatchling will mispackage toolz & tlz packages.

### Tests

The tests in `tests/` serve a few purposes:
- they verify runtime behavior with pytest.
- they verify that these stubs genuinely improve the developer experience in an IDE.
- they are type-checked by basedpyright. This ensures the stubs match actual library behavior.

## Contributing

Contributions are welcome! Areas that could use improvement:

1. More precise generic types
2. Additional overloads for functions with variable signatures
3. Improved curry and composition typing
4. Protocol types for duck-typed parameters

## License

BSD 3-Clause (same as toolz)
