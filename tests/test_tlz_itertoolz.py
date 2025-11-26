"""Tests for tlz.itertoolz to verify stubs work correctly."""

from operator import add

import tlz


def test_first_second_last() -> None:
    """first, second, last should return correct elements."""
    nums = [1, 2, 3, 4, 5]

    f: int = tlz.first(nums)
    s: int = tlz.second(nums)
    la: int = tlz.last(nums)

    assert f == 1
    assert s == 2
    assert la == 5


def test_nth() -> None:
    """nth should return the element at index n."""
    nums = [10, 20, 30, 40]

    result: int = tlz.nth(2, nums)

    assert result == 30


def test_take() -> None:
    """take should return the first n elements."""
    nums = [1, 2, 3, 4, 5]

    taken = tlz.take(3, nums)
    result: list[int] = list(taken)

    assert result == [1, 2, 3]


def test_drop() -> None:
    """drop should skip the first n elements."""
    nums = [1, 2, 3, 4, 5]

    dropped = tlz.drop(2, nums)
    result: list[int] = list(dropped)

    assert result == [3, 4, 5]


def test_take_nth() -> None:
    """take_nth should return every nth element."""
    nums = [0, 1, 2, 3, 4, 5, 6]

    result: list[int] = list(tlz.take_nth(2, nums))

    assert result == [0, 2, 4, 6]


def test_partition() -> None:
    """partition should split sequence into tuples of n."""
    nums = [1, 2, 3, 4, 5, 6]

    parts = tlz.partition(2, nums)
    result: list[tuple[int, ...]] = list(parts)

    assert result == [(1, 2), (3, 4), (5, 6)]


def test_partition_all() -> None:
    """partition_all should include partial final tuple."""
    nums = [1, 2, 3, 4, 5]

    parts = tlz.partition_all(2, nums)
    result: list[tuple[int, ...]] = list(parts)

    assert result == [(1, 2), (3, 4), (5,)]


def test_sliding_window() -> None:
    """sliding_window should return overlapping subsequences."""
    nums = [1, 2, 3, 4]

    windows = tlz.sliding_window(2, nums)
    result: list[tuple[int, ...]] = list(windows)

    assert result == [(1, 2), (2, 3), (3, 4)]


def test_groupby() -> None:
    """groupby should group items by key function."""
    names = ["Alice", "Bob", "Charlie", "Dan"]

    grouped: dict[int, list[str]] = tlz.groupby(len, names)

    assert grouped[3] == ["Bob", "Dan"]
    assert grouped[5] == ["Alice"]
    assert grouped[7] == ["Charlie"]


def test_frequencies() -> None:
    """frequencies should count occurrences."""
    items = ["cat", "dog", "cat", "bird", "cat"]

    freqs: dict[str, int] = tlz.frequencies(items)

    assert freqs["cat"] == 3
    assert freqs["dog"] == 1
    assert freqs["bird"] == 1


def test_unique() -> None:
    """unique should return distinct elements in order."""
    nums = [1, 2, 1, 3, 2, 4, 1]

    result: list[int] = list(tlz.unique(nums))

    assert result == [1, 2, 3, 4]


def test_concat() -> None:
    """concat should concatenate iterables."""
    lists: list[list[int]] = [[1, 2], [3, 4], [5]]

    result: list[int] = list(tlz.concat(lists))

    assert result == [1, 2, 3, 4, 5]


def test_concatv() -> None:
    """concatv should concatenate variadic iterables."""
    result: list[int] = list(tlz.concatv([1, 2], [3, 4], [5]))

    assert result == [1, 2, 3, 4, 5]


def test_interleave() -> None:
    """interleave should alternate between sequences."""
    result: list[int] = list(tlz.interleave([[1, 2, 3], [10, 20, 30]]))

    assert result == [1, 10, 2, 20, 3, 30]


def test_interpose() -> None:
    """interpose should insert element between items."""
    result: list[int | str] = list(tlz.interpose("x", [1, 2, 3]))

    assert result == [1, "x", 2, "x", 3]


def test_get_single() -> None:
    """get with single index should return element."""
    seq = ["a", "b", "c"]

    result: str = tlz.get(1, seq)

    assert result == "b"


def test_get_multiple() -> None:
    """get with multiple indices should return tuple."""
    seq = ["a", "b", "c", "d"]

    result: tuple[str, ...] = tlz.get([0, 2], seq)

    assert result == ("a", "c")


def test_topk() -> None:
    """topk should return the k largest elements."""
    nums = [3, 1, 4, 1, 5, 9, 2, 6]

    result: tuple[int, ...] = tlz.topk(3, nums)

    assert result == (9, 6, 5)


def test_accumulate() -> None:
    """accumulate should compute running totals."""
    nums = [1, 2, 3, 4, 5]

    result: list[int] = list(tlz.accumulate(add, nums))

    assert result == [1, 3, 6, 10, 15]


def test_iterate() -> None:
    """iterate should repeatedly apply function."""

    def inc(x: int) -> int:
        return x + 1

    counter = tlz.iterate(inc, 0)

    result: list[int] = [next(counter) for _ in range(5)]

    assert result == [0, 1, 2, 3, 4]


def test_count() -> None:
    """count should return the number of items."""
    nums = [1, 2, 3, 4, 5]

    result: int = tlz.count(nums)

    assert result == 5


def test_cons() -> None:
    """cons should prepend element to sequence."""
    result: list[int] = list(tlz.cons(0, [1, 2, 3]))

    assert result == [0, 1, 2, 3]


def test_remove() -> None:
    """remove should filter out items matching predicate."""

    def is_even(x: int) -> bool:
        return x % 2 == 0

    result: list[int] = list(tlz.remove(is_even, [1, 2, 3, 4, 5]))

    assert result == [1, 3, 5]


def test_peek() -> None:
    """peek should return first element and full iterator."""
    seq = [1, 2, 3]

    first, iterator = tlz.peek(seq)
    result: list[int] = list(iterator)

    assert first == 1
    assert result == [1, 2, 3]


def test_peekn() -> None:
    """peekn should return first n elements and full iterator."""
    seq = [1, 2, 3, 4, 5]

    first_two, iterator = tlz.peekn(2, seq)
    result: list[int] = list(iterator)

    assert first_two == (1, 2)
    assert result == [1, 2, 3, 4, 5]
