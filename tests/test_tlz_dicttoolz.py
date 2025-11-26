"""Tests for tlz.dicttoolz to verify stubs work correctly."""

import tlz


def test_merge() -> None:
    """merge should combine dictionaries."""
    d1 = {"a": 1, "b": 2}
    d2 = {"c": 3, "d": 4}

    result: dict[str, int] = tlz.merge(d1, d2)

    assert result == {"a": 1, "b": 2, "c": 3, "d": 4}


def test_merge_precedence() -> None:
    """merge should give precedence to later dicts."""
    d1 = {"a": 1, "b": 2}
    d2 = {"b": 20, "c": 3}

    result: dict[str, int] = tlz.merge(d1, d2)

    assert result == {"a": 1, "b": 20, "c": 3}


def test_merge_with() -> None:
    """merge_with should combine values with function."""
    d1 = {"a": 1, "b": 2}
    d2 = {"a": 10, "b": 20}

    result: dict[str, int] = tlz.merge_with(sum, d1, d2)

    assert result == {"a": 11, "b": 22}


def test_valmap() -> None:
    """valmap should transform values."""
    d = {"a": 1, "b": 2, "c": 3}

    doubled: dict[str, int] = tlz.valmap(lambda x: x * 2, d)

    assert doubled == {"a": 2, "b": 4, "c": 6}


def test_valmap_type_change() -> None:
    """valmap should handle type transformations."""
    d = {"a": 1, "b": 2}

    stringified: dict[str, str] = tlz.valmap(str, d)

    assert stringified == {"a": "1", "b": "2"}


def test_keymap() -> None:
    """keymap should transform keys."""
    d = {"alice": 1, "bob": 2}

    result: dict[str, int] = tlz.keymap(str.upper, d)

    assert result == {"ALICE": 1, "BOB": 2}


def test_itemmap() -> None:
    """itemmap should transform key-value pairs."""
    d = {"a": 1, "b": 2}

    # Swap keys and values
    def swap(item: tuple[str, int]) -> tuple[int, str]:
        k, v = item
        return v, k

    result: dict[int, str] = tlz.itemmap(swap, d)

    assert result == {1: "a", 2: "b"}


def test_valfilter() -> None:
    """valfilter should filter by value."""
    d = {"a": 1, "b": 2, "c": 3, "d": 4}

    result: dict[str, int] = tlz.valfilter(lambda x: x > 2, d)

    assert result == {"c": 3, "d": 4}


def test_keyfilter() -> None:
    """keyfilter should filter by key."""
    d = {"apple": 1, "banana": 2, "apricot": 3}

    result: dict[str, int] = tlz.keyfilter(lambda k: k.startswith("a"), d)

    assert result == {"apple": 1, "apricot": 3}


def test_itemfilter() -> None:
    """itemfilter should filter by key-value pair."""
    d = {"a": 1, "b": 2, "c": 3, "d": 4}

    def key_less_than_c_and_val_even(item: tuple[str, int]) -> bool:
        k, v = item
        return k < "c" and v % 2 == 0

    result: dict[str, int] = tlz.itemfilter(key_less_than_c_and_val_even, d)

    assert result == {"b": 2}


def test_assoc() -> None:
    """assoc should add/update a key without mutation."""
    d = {"a": 1, "b": 2}

    result: dict[str, int] = tlz.assoc(d, "c", 3)

    assert result == {"a": 1, "b": 2, "c": 3}
    assert d == {"a": 1, "b": 2}  # original unchanged


def test_dissoc() -> None:
    """dissoc should remove keys without mutation."""
    d = {"a": 1, "b": 2, "c": 3}

    result: dict[str, int] = tlz.dissoc(d, "b")

    assert result == {"a": 1, "c": 3}
    assert d == {"a": 1, "b": 2, "c": 3}  # original unchanged


def test_dissoc_multiple() -> None:
    """dissoc should remove multiple keys."""
    d = {"a": 1, "b": 2, "c": 3, "d": 4}

    result: dict[str, int] = tlz.dissoc(d, "a", "c")

    assert result == {"b": 2, "d": 4}


def test_assoc_in() -> None:
    """assoc_in should set nested values."""
    d: dict[str, dict[str, int]] = {"a": {"b": 1}}

    result = tlz.assoc_in(d, ["a", "c"], 2)

    assert result == {"a": {"b": 1, "c": 2}}


def test_update_in() -> None:
    """update_in should apply function to nested value."""
    d: dict[str, dict[str, int]] = {"a": {"b": 1}}

    def add_ten(x: int) -> int:
        return x + 10

    result = tlz.update_in(d, ["a", "b"], add_ten)

    assert result == {"a": {"b": 11}}


def test_get_in() -> None:
    """get_in should retrieve nested values."""
    d = {"a": {"b": {"c": 42}}}

    result = tlz.get_in(["a", "b", "c"], d)

    assert result == 42


def test_get_in_default() -> None:
    """get_in should return default for missing keys."""
    d = {"a": {"b": 1}}

    result = tlz.get_in(["a", "x"], d, default=-1)

    assert result == -1
