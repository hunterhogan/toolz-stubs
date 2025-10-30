"""Test that our stubs are found by type checkers."""

import tlz

import toolz

# Test basic function
result1 = toolz.identity(42)
result2 = tlz.identity("hello")

# Test compose
composed = toolz.compose(str.upper, str.strip)
text = composed("  hello  ")


# Test curry
@toolz.curry
def add(x: int, y: int) -> int:
    return x + y


add_five = add(5)
result3 = add_five(3)

# These should reveal the types if stubs are working
# (pyright will show these in output)
reveal_type(result1)
reveal_type(result2)
reveal_type(composed)
reveal_type(add_five)
