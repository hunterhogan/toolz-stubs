"""Tests for tlz.functoolz to verify stubs work correctly."""

import tlz


def test_identity() -> None:
    """identity should preserve type and return the same value."""
    x: int = tlz.identity(5)
    s: str = tlz.identity("hello")

    assert x == 5
    assert s == "hello"


def test_compose() -> None:
    """compose should chain functions right-to-left."""
    composed = tlz.compose(str.upper, str.strip)
    result: str = composed("  hello  ")

    assert result == "HELLO"


def test_compose_left() -> None:
    """compose_left should chain functions left-to-right."""
    composed = tlz.compose_left(str.strip, str.upper)
    result: str = composed("  hello world  ")

    assert result == "HELLO WORLD"


def test_compose_multi() -> None:
    """compose with multiple functions should chain correctly."""
    composed = tlz.compose(len, str.upper, str.strip)
    result: int = composed("  hello  ")

    assert result == 5


def test_pipe() -> None:
    """pipe should thread value through functions."""
    result: str = tlz.pipe("  hello  ", str.strip, str.upper)

    assert result == "HELLO"


def test_pipe_type_transformation() -> None:
    """pipe should handle type transformations."""
    result: int = tlz.pipe("hello", str.upper, len)

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
    result: tuple[int, ...] = j(10)

    assert result == (11, 20)


def test_do() -> None:
    """do should call function for side effects and return input."""
    log: list[int] = []
    result: int = tlz.do(log.append, 42)

    assert result == 42
    assert log == [42]


def test_apply() -> None:
    """apply should call function with provided arguments."""

    def add(x: int, y: int) -> int:
        return x + y

    result: int = tlz.apply(add, 2, 3)

    assert result == 5
