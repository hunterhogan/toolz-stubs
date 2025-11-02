# Partial Stub Package Installation Investigation

## The Problem

When developing type stubs for an existing package like `toolz`, we ran into issues getting basedpyright to recognize our stub files during development and testing.

## Background: Partial Stub Packages

According to [PEP 561](https://peps.python.org/pep-0561/#partial-stub-packages), partial stub packages are stub packages that install `.pyi` files directly into an existing package's directory structure:

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
```

### How Type Checkers Resolve Imports

When a type checker sees `import toolz`, it looks in this order:
1. **Inline types or stubs within the package** (`toolz/*.pyi` with `py.typed` marker)
2. **Separate stub packages** (`toolz-stubs` package)
3. **Typeshed** (for standard library)

## The Installation Problem

### What We Tried

1. **Built the wheel correctly** - The wheel contains the stub files in the right structure:
   ```
   Archive:  dist/toolz_stubs-0.1.0-py3-none-any.whl
     toolz/__init__.pyi
     toolz/dicttoolz.pyi
     toolz/functoolz.pyi
     toolz/curried/__init__.pyi
     toolz/py.typed
     ...
   ```

2. **Installed the wheel** - But the stub files weren't placed into the existing `toolz` package:
   ```bash
   $ uv pip install dist/toolz_stubs-0.1.0-py3-none-any.whl
   $ ls /path/to/site-packages/toolz/*.pyi
   # No files found!
   ```

3. **Checked the installation record**:
   ```bash
   $ cat site-packages/toolz_stubs-0.1.0.dist-info/RECORD
   _toolz_stubs.pth,sha256=...,0
   toolz_stubs-0.1.0.dist-info/INSTALLER,...
   toolz_stubs-0.1.0.dist-info/METADATA,...
   # No .pyi files listed!
   ```

### Root Cause

**pip/uv will not install files into a directory owned by another package.**

The `toolz` directory in site-packages is owned by the `toolz` package distribution. When we try to install `toolz-stubs`, pip/uv refuses to place files into that directory because it would create a conflict - two packages claiming ownership of the same files.

This is a fundamental limitation of the standard Python packaging tools for partial stub packages.

## The Solution for Development

Since we can't install the stubs in the "correct" location during development, we need to tell basedpyright where to find them.

### Using `executionEnvironments` in pyrightconfig.json

```json
{
  "pythonVersion": "3.12",
  "include": ["src/**/*", "tests/**/*", "type_tests/**/*"],
  "executionEnvironments": [
    {
      "root": "tests",
      "extraPaths": ["src"]
    },
    {
      "root": "type_tests",
      "extraPaths": ["src"]
    },
    {
      "root": "src"
    }
  ]
}
```

This configuration:
- Creates separate execution environments for `tests/`, `type_tests/`, and `src/`
- Adds `src/` to the module search path for the test environments
- Allows basedpyright to find `src/toolz/*.pyi` when analyzing test files that import `toolz`

### Why This Works

When basedpyright analyzes a file in `tests/`, it:
1. Uses the execution environment with `"root": "tests"`
2. Adds `src/` to the module search path via `extraPaths`
3. When it sees `import toolz.curried`, it searches in order:
   - `src/toolz/curried/__init__.pyi` ← **Found!**
   - `site-packages/toolz/curried/__init__.pyi` (would be checked if above didn't exist)
4. Uses our local stub file instead of looking in site-packages

## Results

Before the fix:
```
tests/test_curried.py:5:21 - error: "pipe" is not a known attribute of module "toolz.curried"
2 errors, 5 warnings, 0 notes
```

After the fix:
```
tests/test_curried.py
0 errors, 5 warnings, 0 notes
```

The remaining warnings are about type inference in complex curried pipelines, not about missing stubs.

## Alternative Approaches Considered

### 1. `stubPath` Configuration
```json
{"stubPath": "src"}
```
- **Doesn't work**: `stubPath` is for `-stubs` packages (separate stub packages)
- Our stubs are partial stubs (meant to be installed alongside the package)

### 2. `extraPaths` at Root Level
```json
{"extraPaths": ["src"]}
```
- **Doesn't work reliably**: Module resolution still prefers site-packages
- Type checker finds the runtime `.py` files before our `.pyi` files

### 3. Symlinks
Create symlinks from site-packages to our local stubs:
```bash
ln -s /path/to/project/src/toolz/*.pyi /path/to/site-packages/toolz/
```
- **Works but fragile**: Requires manual setup, breaks on venv recreation
- Not suitable for CI/CD or team development

### 4. Post-Install Hook
Use a post-install script to copy `.pyi` files:
```python
# setup.py or pyproject.toml
[tool.hatch.build.hooks.custom]
# Copy .pyi files to target package
```
- **Works for actual installation**: Good for end users
- **Doesn't help during development**: Still need config for local testing

## Production Installation Strategy

For actual users installing the package (not development), we need a different approach. Options:

### Option A: Post-Install Script
Use a build hook or post-install script to copy `.pyi` files into the installed `toolz` package.

**Pros:**
- Achieves the intended partial stub structure
- Type checkers find stubs automatically

**Cons:**
- Complex build configuration
- May violate some package manager assumptions
- Could break with pip's future changes

### Option B: Separate Stub Package
Change to a `-stubs` package approach:
```
site-packages/
  toolz/           # Original package
  toolz-stubs/     # Our stubs package
```

**Pros:**
- Standard PEP 561 approach
- No installation conflicts
- Works with all package managers

**Cons:**
- Doesn't follow our "partial stubs" design
- Less clean for users (two packages)
- Type checkers check `-stubs` packages last (after inline stubs)

### Option C: Hybrid Approach
- Development: Use `executionEnvironments` (current solution)
- Distribution: Use post-install hook or custom installer

**Pros:**
- Best of both worlds
- Flexible for different use cases

**Cons:**
- More complex to maintain
- Users might need special installation instructions

## Recommendations

### For Development (Current State)
✅ Use `executionEnvironments` with `extraPaths` in `pyrightconfig.json`
- Works reliably
- No manual intervention needed
- Clean separation of concerns

### For Distribution (Future Work)
Consider these options in priority order:

1. **Test with actual `pip install`** from a clean environment
   - Build the wheel
   - Install in a fresh venv (without `toolz` pre-installed)
   - Check if stubs are placed correctly when both packages install together

2. **If that doesn't work**, add a custom build hook:
   - Use `hatchling` build hooks to copy files post-installation
   - Document the installation process clearly

3. **If build hooks are too fragile**, switch to `-stubs` package:
   - Change package name to `toolz-stubs`
   - Install as a separate package
   - Update documentation to reflect the change

## References

- [PEP 561 - Distributing and Packaging Type Information](https://peps.python.org/pep-0561/)
- [Typing specification - Distributing Type Information](https://typing.python.org/en/latest/spec/distributing.html#partial-stub-packages)
- [Pyright Configuration Options](https://microsoft.github.io/pyright/#/configuration)
