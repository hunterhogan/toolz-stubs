from typing import assert_type

import tlz
import toolz


def test_basic_identity():
    """Type checker should correctly infer types for identity."""
    x = toolz.identity(5)
    _ = assert_type(x, int)

    y = tlz.identity("hello")
    _ = assert_type(y, str)


def test_compose_left():
    composed_func = toolz.compose_left(str.strip, str.upper)
    result = composed_func("  hello world  ")
    assert result == "HELLO WORLD"


def test_compose():
    """Test compose with type assertions."""
    composed = toolz.compose(str.upper, str.strip)
    _ = assert_type(composed("  hello  "), str)


# TODO: curry typing needs improvement - add(5) returns int | curry[int]
# which makes add_five(3) error because int isn't callable
# @toolz.curry
# def add(x: int, y: int) -> int:
#     return x + y
# add_five = add(5)
# result3 = add_five(3)
