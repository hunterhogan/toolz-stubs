import toolz


def test_basic_identity():
    """
    Our type checker, when running these tests, should correctly infer types.
    """
    # Test that type checkers recognize our stubs
    x = toolz.identity(5)
    # y = tlz.identity(10)
    # z = cytoolz.identity(15)

    def function_accepts_only_ints(x: int) -> None:
        assert isinstance(x, int)

    function_accepts_only_ints(x)

    # assert typing.reveal_type(x) is int
    # assert typing.reveal_type(y) is int


def test_compose_left():
    composed_func = toolz.compose_left(str.strip, str.upper)
    result = composed_func("  hello world  ")
    assert result == "HELLO WORLD"
