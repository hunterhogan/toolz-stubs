import toolz.curried as curr


def test_basic_curry_func():
    a_result = curr.pipe(range(5), curr.map(lambda x: x + 1), curr.map(str), list)

    def cvt_list_of_strings_to_tuple(some_list: list[str]) -> tuple[str, ...]:
        return tuple(some_list)

    tuple_result = cvt_list_of_strings_to_tuple(a_result)
