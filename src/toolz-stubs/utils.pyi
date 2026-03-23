import collections.abc

def raises(err: type[Exception], lamda: collections.abc.Callable[[], None]) -> bool: ...

no_default = "__no__default__"
