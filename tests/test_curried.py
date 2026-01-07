"""Tests for toolz.curried to verify stubs work correctly."""

from collections.abc import Iterator
from typing import assert_type

import toolz.curried as curr


class TestMapcat:
    """Tests for curried mapcat function."""

    def test_can_expand(self) -> None:
        """mapcat should work with functions that expand elements."""

        def possibly_expands(item: int | list[int]) -> list[int]:
            if isinstance(item, int):
                return [item, item]
            return item

        result = curr.mapcat(possibly_expands, [1, [2, 3], 4])

        _ = assert_type(result, Iterator[int])
        assert list(result) == [1, 1, 2, 3, 4, 4]


def test_basic_curry_func() -> None:
    """Curried pipe should correctly infer list[str] output type."""

    def add_one(i: int) -> int:
        return i + 1

    a_result = curr.pipe(range(5), curr.map(add_one), curr.map(str), list)

    _ = assert_type(a_result, list[str])
    assert a_result == ["1", "2", "3", "4", "5"]


class TestSorted:
    def test_can_type_comparable(self) -> None:
        """From https://github.com/mgrinshpon/toolz-stubs/issues/34"""

        def mod_3(x: int) -> int:
            return x % 3

        result = curr.pipe(range(10), curr.sorted(key=mod_3), list)
        _ = assert_type(result, list[int])
        assert result == [0, 3, 6, 9, 1, 4, 7, 2, 5, 8]
