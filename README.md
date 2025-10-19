# toolz-stubs

Type stubs for [toolz](https://github.com/pytoolz/toolz), [cytoolz](https://github.com/pytoolz/cytoolz), and [tlz](https://github.com/pytoolz/toolz/tree/main/tlz) - Python functional programming libraries.

## What This Package Provides

This package provides type stubs (`.pyi` files) for:
- **toolz**: The pure Python functional programming library
- **cytoolz**: The Cython-accelerated version with identical API
- **tlz**: The auto-selecting wrapper that uses cytoolz (if available) or falls back to toolz

## Design Approach: Partial Stubs

This package uses [PEP 561's "partial stubs"](https://peps.python.org/pep-0561/#partial-stub-packages) approach. Instead of being a separate `*-stubs` package that sits alongside the main package, [we install stub files directly into the package directories](https://typing.python.org/en/latest/spec/distributing.html#partial-stub-packages):

```
site-packages/
  toolz-stubs/        # Package metadata only
  toolz/
    __init__.py       # Original toolz files
    __init__.pyi      # Our stub files
    functoolz.pyi
    itertoolz.pyi
    ...
    py.typed          # Marker for partial stubs
  cytoolz/
    __init__.py       # Original cytoolz files
    __init__.pyi      # Our stub files (identical to toolz)
    ...
    py.typed          # Marker for partial stubs
  tlz/
    __init__.py       # Original tlz files
    __init__.pyi      # Our stub files (identical to toolz)
    ...
    py.typed          # Marker for partial stubs
```

### Why This Approach?

When type checkers look for type information for `import toolz`, they check in this order:
1. **Inline types or stubs within the package** (`toolz/*.pyi` with `py.typed` marker)
2. **Separate stub packages** (`toolz-stubs` package)
3. **Typeshed** (for standard library)

By installing partial stubs directly into the package directories, we ensure type checkers find our stubs first.

## Alternative Approaches Considered

### 1. Separate Stub Packages
**Structure:** Create `toolz-stubs`, `cytoolz-stubs`, and `tlz-stubs` as three separate packages.

**Pros:**
- Follows the most common PEP 561 convention
- Each package can be versioned independently

**Cons:**
- Massive duplication since all three have identical APIs
- Triple maintenance burden
- `cytoolz-stubs` already exists on PyPI (conflict)

### 2. Single Unified Package
**Structure:** Single `pytoolz-stubs` package providing stubs for all three.

**Pros:**
- Single source of truth
- Easier maintenance

**Cons:**
- Not standard PEP 561 - would require manual type checker configuration
- Users would need to add custom `stubPath` settings

### 3. Monorepo with Build-time Split
**Structure:** Single source, build process creates three packages.

**Pros:**
- Single source of truth in repository
- Standard PEP 561 packages for distribution

**Cons:**
- Complex build process
- Still conflicts with existing `cytoolz-stubs`

## Why We Include cytoolz

While there's a `cytoolz-stubs` package on PyPI, it hasn't been updated in 6 years (last update in 2018). Rather than leave cytoolz users with outdated type information, we provide modern, maintained stubs for all three packages:
- **toolz**: The pure Python implementation
- **cytoolz**: The Cython-accelerated version
- **tlz**: The auto-selecting wrapper

Since all three have identical APIs, we maintain a single source of truth for the type definitions.

## Installation

```bash
pip install toolz-stubs
```

This will install type stubs for `toolz`, `cytoolz`, and `tlz`.

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

## Development

### Project Structure

```
toolz-stubs/
  src/
    toolz/          # Stubs for toolz
      __init__.pyi
      functoolz.pyi
      itertoolz.pyi
      dicttoolz.pyi
      recipes.pyi
      utils.pyi
      py.typed
      curried/
        __init__.pyi
    cytoolz/        # Identical stubs for cytoolz
      ...
    tlz/            # Identical stubs for tlz
      ...
  pyproject.toml
  README.md
```

### Building

```bash
uv build
```

This creates a wheel that, when installed, places stub files into `toolz/`, `cytoolz/`, and `tlz/` directories in site-packages.

### Type Checking

```bash
uv run basedpyright
```

## Technical Details

### PYPY Variable
The stubs include a `PYPY` boolean variable that indicates whether code is running on PyPy vs CPython. This is used internally by toolz for implementation differences between Python interpreters.

### Curry Decorator
The `curry` decorator is both a class and a decorator, making it complex to type. The stubs provide proper typing for both use cases.

### Dynamic Module Loading (tlz)
The `tlz` package uses Python's import machinery to dynamically choose between cytoolz and toolz at runtime. Our stubs provide static types for tlz that match the shared API.

## Contributing

Contributions are welcome! The main areas that need work:
1. Adding more precise generic types
2. Adding overloads for functions with variable signatures
3. Improving curry and composition typing
4. Adding protocol types for duck-typed parameters

## License

[Same as toolz - BSD 3-Clause]
