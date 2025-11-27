"""Tests for toolz.curried to verify stubs work correctly."""

from typing import assert_type

import toolz.curried as curr


def test_basic_curry_func() -> None:
    """Curried pipe should correctly infer list[str] output type."""

    def add_one(i: int) -> int:
        return i + 1

    a_result = curr.pipe(range(5), curr.map(add_one), curr.map(str), list)

    _ = assert_type(a_result, list[str])
    assert a_result == ["1", "2", "3", "4", "5"]
