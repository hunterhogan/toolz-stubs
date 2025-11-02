import toolz.curried as curr


def test_basic_curry_func():
    def add_one(i: int) -> int:
        return i + 1

    a_result = curr.pipe(range(5), curr.map(add_one), curr.map(str), list)

    def cvt_list_of_strings_to_tuple(some_list: list[str]) -> tuple[str, ...]:
        return tuple(some_list)

    tuple_result = cvt_list_of_strings_to_tuple(a_result)
    assert tuple_result == ("1", "2", "3", "4", "5")
