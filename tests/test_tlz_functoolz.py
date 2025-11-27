"""Tests for tlz.functoolz to verify stubs work correctly."""

from typing import assert_type

import tlz


def test_identity() -> None:
    """identity should preserve type and return the same value."""
    x = tlz.identity(5)
    s = tlz.identity("hello")

    _ = assert_type(x, int)
    _ = assert_type(s, str)
    assert x == 5
    assert s == "hello"


def test_compose() -> None:
    """compose should chain functions right-to-left."""
    composed = tlz.compose(str.upper, str.strip)
    result = composed("  hello  ")

    _ = assert_type(result, str)
    assert result == "HELLO"


def test_compose_left() -> None:
    """compose_left should chain functions left-to-right."""
    composed = tlz.compose_left(str.strip, str.upper)
    result = composed("  hello world  ")

    _ = assert_type(result, str)
    assert result == "HELLO WORLD"


def test_compose_multi() -> None:
    """compose with multiple functions should chain correctly."""
    composed = tlz.compose(len, str.upper, str.strip)
    result = composed("  hello  ")

    _ = assert_type(result, int)
    assert result == 5


def test_pipe() -> None:
    """pipe should thread value through functions."""
    result = tlz.pipe("  hello  ", str.strip, str.upper)

    _ = assert_type(result, str)
    assert result == "HELLO"


def test_pipe_type_transformation() -> None:
    """pipe should handle type transformations."""
    result = tlz.pipe("hello", str.upper, len)

    _ = assert_type(result, int)
    assert result == 5


def test_complement() -> None:
    """complement should negate a predicate."""

    def is_even(x: int) -> bool:
        return x % 2 == 0

    is_odd = tlz.complement(is_even)

    assert is_odd(3) is True
    assert is_odd(4) is False


def test_juxt() -> None:
    """juxt should apply multiple functions and return a tuple."""

    def inc(x: int) -> int:
        return x + 1

    def double(x: int) -> int:
        return x * 2

    j = tlz.juxt(inc, double)
    result = j(10)

    _ = assert_type(result, tuple[int, ...])
    assert result == (11, 20)


def test_do() -> None:
    """do should call function for side effects and return input."""
    log: list[int] = []
    result = tlz.do(log.append, 42)

    _ = assert_type(result, int)
    assert result == 42
    assert log == [42]


def test_apply() -> None:
    """apply should call function with provided arguments."""

    def add(x: int, y: int) -> int:
        return x + y

    result = tlz.apply(add, 2, 3)

    _ = assert_type(result, int)
    assert result == 5
