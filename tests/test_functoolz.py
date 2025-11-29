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


class TestJuxt:
    """Tests for juxt function."""

    def test_basic(self) -> None:
        """juxt should apply multiple functions and return a tuple."""

        def inc(x: int) -> int:
            return x + 1

        def double(x: int) -> int:
            return x * 2

        j = toolz.juxt(inc, double)
        result = j(10)

        _ = assert_type(result, tuple[int, int])
        assert result == (11, 20)

    def test_single_function(self) -> None:
        """juxt with single function should return single-element tuple."""

        def inc(x: int) -> int:
            return x + 1

        j = toolz.juxt(inc)
        result = j(10)

        _ = assert_type(result, tuple[int])
        assert result == (11,)

    def test_heterogeneous(self) -> None:
        """juxt should support functions with different return types."""

        def to_str(x: int) -> str:
            return str(x)

        def to_float(x: int) -> float:
            return float(x)

        def identity(x: int) -> int:
            return x

        j = toolz.juxt(to_str, to_float, identity)
        result = j(42)

        _ = assert_type(result, tuple[str, float, int])
        assert result == ("42", 42.0, 42)

    def test_list_input(self) -> None:
        """juxt should accept a list of functions (less precise typing)."""

        def inc(x: int) -> int:
            return x + 1

        def double(x: int) -> int:
            return x * 2

        funcs = [inc, double]
        j = toolz.juxt(funcs)
        result = j(10)

        # List input can't have precise tuple length at type-check time
        _ = assert_type(result, tuple[int, ...])
        assert result == (11, 20)

    def test_empty(self) -> None:
        """juxt with no functions should return empty tuple."""
        j = toolz.juxt()
        result = j(10)

        _ = assert_type(result, tuple[()])
        assert result == ()
