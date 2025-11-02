# pyright: reportUnusedImport=false, reportAny=false
# According to PEP561, file structure should mirror the package structure
# That's why this is in curried/__init__.pyi and not just curried.pyi
import collections.abc
import typing

from typing_extensions import TypeIs

import toolz
from toolz import (
    apply as apply,
    comp as comp,
    complement as complement,
    compose as compose,
    compose_left as compose_left,
    concat as concat,
    concatv as concatv,
    count as count,
    curry as curry,
    diff as diff,
    first as first,
    flip as flip,
    frequencies as frequencies,
    identity as identity,
    interleave as interleave,
    isdistinct as isdistinct,
    isiterable as isiterable,
    juxt as juxt,
    last as last,
    memoize as memoize,
    merge_sorted as merge_sorted,
    peek as peek,
    pipe as pipe,
    second as second,
    thread_first as thread_first,
    thread_last as thread_last,
)

# All functions from operator module are re-exported here.
# Binary and n-ary functions are curried; unary functions are not.
# From a typing perspective, curried functions have identical signatures.
from . import operator
from .exceptions import merge, merge_with

class _Comparable(typing.Protocol):
    def __lt__(self, other: _Comparable) -> bool: ...

# Curried accumulate with explicit overloads for type safety
# Stage 0: No arguments - returns a callable
@typing.overload
def accumulate[T]() -> typing.Callable[..., collections.abc.Iterator[T]]: ...

# Stage 1: Just binop - returns callable waiting for seq (and optional initial)
@typing.overload
def accumulate[T](
    binop: typing.Callable[[T, T], T], /
) -> typing.Callable[..., collections.abc.Iterator[T]]: ...

# Stage 2a: binop + seq (no initial) - executes immediately
@typing.overload
def accumulate[T](
    binop: typing.Callable[[T, T], T], seq: collections.abc.Iterable[T], /
) -> collections.abc.Iterator[T]: ...

# Stage 2b: binop + seq + initial - executes immediately
@typing.overload
def accumulate[T](
    binop: typing.Callable[[T, T], T],
    seq: collections.abc.Iterable[T],
    initial: T,
    /,
) -> collections.abc.Iterator[T]: ...
def accumulate[T](
    binop: typing.Callable[[T, T], T] = ...,
    seq: collections.abc.Iterable[T] = ...,
    initial: T = ...,
) -> collections.abc.Iterator[T] | typing.Callable[..., collections.abc.Iterator[T]]:
    """Curried version of accumulate

    Repeatedly apply binary function to a sequence, accumulating results.

    >>> from toolz.curried import accumulate
    >>> from operator import add, mul
    >>> list(accumulate(add, [1, 2, 3, 4, 5]))
    [1, 3, 6, 10, 15]
    >>> list(accumulate(mul, [1, 2, 3, 4, 5]))
    [1, 2, 6, 24, 120]

    Can be partially applied:
    >>> cumsum = accumulate(add)
    >>> list(cumsum([1, 2, 3, 4, 5]))
    [1, 3, 6, 10, 15]

    With initial value:
    >>> list(accumulate(add, [1, 2, 3], -1))
    [-1, 0, 2, 5]
    >>> list(accumulate(add, [], 1))
    [1]

    Common pattern for cumulative operations:
    >>> from toolz.curried import pipe
    >>> from operator import mul
    >>> cumprod = accumulate(mul)
    >>> list(pipe([1, 2, 3, 4], cumprod))
    [1, 2, 6, 24]

    See Also:
        reduce
        itertools.accumulate
    """
    ...

@typing.overload
def assoc[K, V]() -> typing.Callable[
    ..., dict[K, V] | collections.abc.MutableMapping[K, V]
]: ...
@typing.overload
def assoc[K, V](
    d: collections.abc.Mapping[K, V], /
) -> typing.Callable[..., dict[K, V] | collections.abc.MutableMapping[K, V]]: ...
@typing.overload
def assoc[K, V](
    d: collections.abc.Mapping[K, V], key: K, /
) -> typing.Callable[[V], dict[K, V]]: ...
@typing.overload
def assoc[K, V](
    d: collections.abc.Mapping[K, V],
    key: K,
    /,
    *,
    factory: typing.Callable[[], collections.abc.MutableMapping[K, V]],
) -> typing.Callable[[V], collections.abc.MutableMapping[K, V]]: ...
@typing.overload
def assoc[K, V](
    d: collections.abc.Mapping[K, V], key: K, value: V, /
) -> dict[K, V]: ...
@typing.overload
def assoc[K, V](
    d: collections.abc.Mapping[K, V],
    key: K,
    value: V,
    /,
    *,
    factory: typing.Callable[[], collections.abc.MutableMapping[K, V]],
) -> collections.abc.MutableMapping[K, V]: ...
def assoc[K, V](
    d: collections.abc.Mapping[K, V] = ...,
    key: K = ...,
    value: V = ...,
    *,
    factory: typing.Callable[[], collections.abc.MutableMapping[K, V]] = dict,
) -> (
    dict[K, V]
    | collections.abc.MutableMapping[K, V]
    | typing.Callable[..., dict[K, V] | collections.abc.MutableMapping[K, V]]
):
    """Curried version of assoc

    Return a new dict with new key value pair.

    Does not modify the initial dictionary.

    >>> from toolz.curried import assoc
    >>> d = {'x': 1}
    >>> assoc(d, 'y', 2)
    {'x': 1, 'y': 2}

    Can be partially applied:
    >>> add_y = assoc(d, 'y')
    >>> add_y(2)
    {'x': 1, 'y': 2}

    Common pattern for updating dicts immutably:
    >>> user = {'name': 'Alice', 'age': 30}
    >>> updated = assoc(user, 'age', 31)
    >>> updated
    {'name': 'Alice', 'age': 31}
    >>> user  # Original unchanged
    {'name': 'Alice', 'age': 30}

    Partially applied for mapping:
    >>> from toolz.curried import map
    >>> users = [{'name': 'Alice'}, {'name': 'Bob'}]
    >>> list(map(lambda u: assoc(u, 'active', True), users))
    [{'name': 'Alice', 'active': True}, {'name': 'Bob', 'active': True}]

    See Also:
        dissoc
        update_in
        assoc_in
    """
    ...

assoc_in = toolz.curry(toolz.assoc_in)
cons = toolz.curry(toolz.cons)
countby = toolz.curry(toolz.countby)
dissoc = toolz.curry(toolz.dissoc)
do = toolz.curry(toolz.do)

@typing.overload
def drop[T]() -> typing.Callable[..., collections.abc.Iterator[T]]: ...
@typing.overload
def drop[T](
    n: int, /
) -> typing.Callable[[collections.abc.Iterable[T]], collections.abc.Iterator[T]]: ...
@typing.overload
def drop[T](
    n: int, seq: collections.abc.Iterable[T], /
) -> collections.abc.Iterator[T]: ...
def drop[T](
    n: int = ..., seq: collections.abc.Iterable[T] = ...
) -> (
    collections.abc.Iterator[T]
    | typing.Callable[[collections.abc.Iterable[T]], collections.abc.Iterator[T]]
    | typing.Callable[..., collections.abc.Iterator[T]]
):
    """Curried version of drop

    The sequence following the first n elements.

    >>> from toolz.curried import drop
    >>> list(drop(2, [10, 20, 30, 40, 50]))
    [30, 40, 50]

    Can be partially applied:
    >>> drop_two = drop(2)
    >>> list(drop_two([10, 20, 30, 40, 50]))
    [30, 40, 50]

    Common pattern for skipping headers:
    >>> from toolz.curried import pipe
    >>> data = [['header1', 'header2'], ['a', 'b'], ['c', 'd']]
    >>> list(drop(1, data))
    [['a', 'b'], ['c', 'd']]

    See Also:
        take
        tail
    """
    ...

@typing.overload
def excepts[T, **P]() -> typing.Callable[..., toolz.excepts[T, P]]: ...
@typing.overload
def excepts[T, **P](
    exc: type[Exception] | tuple[type[Exception], ...], /
) -> (
    typing.Callable[[typing.Callable[P, T]], toolz.excepts[T, P]]
    | typing.Callable[
        [typing.Callable[P, T], typing.Callable[[Exception], T]], toolz.excepts[T, P]
    ]
): ...
@typing.overload
def excepts[T, **P](
    exc: type[Exception] | tuple[type[Exception], ...],
    func: typing.Callable[P, T],
    /,
) -> toolz.excepts[T, P]: ...
@typing.overload
def excepts[T, **P](
    exc: type[Exception] | tuple[type[Exception], ...],
    func: typing.Callable[P, T],
    handler: typing.Callable[[Exception], T],
    /,
) -> toolz.excepts[T, P]: ...
def excepts[T, **P](
    exc: type[Exception] | tuple[type[Exception], ...] = ...,
    func: typing.Callable[P, T] = ...,
    handler: typing.Callable[[Exception], T] | None = ...,
) -> toolz.excepts[T, P] | typing.Callable[..., toolz.excepts[T, P]]:
    """Curried version of excepts

    A wrapper around a function to catch exceptions and dispatch to a handler.

    This is like a functional try/except block.

    >>> from toolz.curried import excepts
    >>> excepting = excepts(
    ...     ValueError,
    ...     lambda a: [1, 2].index(a),
    ...     lambda _: -1,
    ... )
    >>> excepting(1)
    0
    >>> excepting(3)
    -1

    Can be partially applied:
    >>> handle_value_error = excepts(ValueError)
    >>> safe_index = handle_value_error(lambda a: [1, 2].index(a), lambda _: -1)
    >>> safe_index(1)
    0
    >>> safe_index(3)
    -1

    Multiple exceptions:
    >>> excepting = excepts((IndexError, KeyError), lambda a: a[0])
    >>> excepting([1])
    1
    >>> excepting([])  # Returns None (default handler)

    Common pattern for safe operations:
    >>> from toolz.curried import pipe
    >>> safe_int = excepts(ValueError, int, lambda _: 0)
    >>> safe_int("123")
    123
    >>> safe_int("abc")
    0

    See Also:
        do
        complement
    """
    ...

@typing.overload
def filter[T]() -> typing.Callable[
    ..., collections.abc.Iterator[T] | typing.Callable[..., collections.abc.Iterator[T]]
]: ...
@typing.overload
def filter[T](
    function: None, /
) -> typing.Callable[
    [collections.abc.Iterable[T | None]], collections.abc.Iterator[T]
]: ...
@typing.overload
def filter[S, T](
    function: typing.Callable[[S], typing.TypeGuard[T]], /
) -> typing.Callable[[collections.abc.Iterable[S]], collections.abc.Iterator[T]]: ...
@typing.overload
def filter[S, T](
    function: typing.Callable[[S], TypeIs[T]], /
) -> typing.Callable[[collections.abc.Iterable[S]], collections.abc.Iterator[T]]: ...
@typing.overload
def filter[T](
    function: typing.Callable[[T], typing.Any], /
) -> typing.Callable[[collections.abc.Iterable[T]], collections.abc.Iterator[T]]: ...
@typing.overload
def filter[T](
    function: None, iterable: collections.abc.Iterable[T | None], /
) -> collections.abc.Iterator[T]: ...
@typing.overload
def filter[S, T](
    function: typing.Callable[[S], typing.TypeGuard[T]],
    iterable: collections.abc.Iterable[S],
    /,
) -> collections.abc.Iterator[T]: ...
@typing.overload
def filter[S, T](
    function: typing.Callable[[S], TypeIs[T]],
    iterable: collections.abc.Iterable[S],
    /,
) -> collections.abc.Iterator[T]: ...
@typing.overload
def filter[T](
    function: typing.Callable[[T], typing.Any],
    iterable: collections.abc.Iterable[T],
    /,
) -> collections.abc.Iterator[T]: ...
def filter[T](
    function: typing.Callable[[T], typing.Any] | None = ...,
    iterable: collections.abc.Iterable[T] = ...,
) -> (
    collections.abc.Iterator[T]
    | typing.Callable[[collections.abc.Iterable[T]], collections.abc.Iterator[T]]
    | typing.Callable[
        ...,
        collections.abc.Iterator[T] | typing.Callable[..., collections.abc.Iterator[T]],
    ]
):
    """Curried version of builtin filter function

    Return elements from an iterable where the predicate is true.

    >>> from toolz.curried import filter
    >>> is_even = lambda x: x % 2 == 0
    >>> list(filter(is_even, [1, 2, 3, 4, 5]))
    [2, 4]

    Can be partially applied:
    >>> filter_even = filter(is_even)
    >>> list(filter_even([1, 2, 3, 4, 5]))
    [2, 4]

    Filter with None removes falsy values:
    >>> list(filter(None, [0, 1, False, True, '', 'hello']))
    [1, True, 'hello']
    """
    ...

@typing.overload
def get[T]() -> typing.Callable[..., T | tuple[T, ...]]: ...
@typing.overload
def get[T](
    ind: collections.abc.Sequence[typing.Any], /
) -> (
    typing.Callable[
        [collections.abc.Sequence[T] | collections.abc.Mapping[typing.Any, T]],
        tuple[T, ...],
    ]
    | typing.Callable[
        [collections.abc.Sequence[T] | collections.abc.Mapping[typing.Any, T], T],
        tuple[T, ...],
    ]
): ...
@typing.overload
def get[T](
    ind: typing.Any, /
) -> (
    typing.Callable[
        [collections.abc.Sequence[T] | collections.abc.Mapping[typing.Any, T]], T
    ]
    | typing.Callable[
        [collections.abc.Sequence[T] | collections.abc.Mapping[typing.Any, T], T], T
    ]
): ...
@typing.overload
def get[T](
    ind: collections.abc.Sequence[typing.Any],
    seq: collections.abc.Sequence[T] | collections.abc.Mapping[typing.Any, T],
    /,
) -> tuple[T, ...]: ...
@typing.overload
def get[T](
    ind: typing.Any,
    seq: collections.abc.Sequence[T] | collections.abc.Mapping[typing.Any, T],
    /,
) -> T: ...
@typing.overload
def get[T](
    ind: collections.abc.Sequence[typing.Any],
    seq: collections.abc.Sequence[T] | collections.abc.Mapping[typing.Any, T],
    default: T,
    /,
) -> tuple[T, ...]: ...
@typing.overload
def get[T](
    ind: typing.Any,
    seq: collections.abc.Sequence[T] | collections.abc.Mapping[typing.Any, T],
    default: T,
    /,
) -> T: ...
def get[T](
    ind: typing.Any | collections.abc.Sequence[typing.Any] = ...,
    seq: collections.abc.Sequence[T] | collections.abc.Mapping[typing.Any, T] = ...,
    default: T = ...,
) -> T | tuple[T, ...] | typing.Callable[..., T | tuple[T, ...]]:
    """Curried version of get

    Get element(s) from a sequence or dict.

    >>> from toolz.curried import get
    >>> get(1, 'ABC')
    'B'

    Can be partially applied:
    >>> get_first = get(0)
    >>> get_first([1, 2, 3])
    1

    Get multiple values:
    >>> get([0, 2], 'ABC')
    ('A', 'C')

    Works with dicts:
    >>> phonebook = {'Alice': '555-1234', 'Bob': '555-5678'}
    >>> get('Alice', phonebook)
    '555-1234'

    Partially applied for mapping:
    >>> from toolz.curried import map
    >>> people = [{'name': 'Alice'}, {'name': 'Bob'}]
    >>> list(map(get('name'), people))
    ['Alice', 'Bob']

    With defaults:
    >>> get('Charlie', phonebook, 'N/A')
    'N/A'
    """
    ...

get_in = toolz.curry(toolz.get_in)

@typing.overload
def groupby[KT, T]() -> typing.Callable[..., dict[KT, list[T]]]: ...
@typing.overload
def groupby[KT, T](
    key: typing.Callable[[T], KT], /
) -> typing.Callable[[collections.abc.Iterable[T]], dict[KT, list[T]]]: ...
@typing.overload
def groupby[T](
    key: typing.Any, /
) -> typing.Callable[[collections.abc.Iterable[T]], dict[typing.Any, list[T]]]: ...
@typing.overload
def groupby[KT, T](
    key: typing.Callable[[T], KT], seq: collections.abc.Iterable[T], /
) -> dict[KT, list[T]]: ...
@typing.overload
def groupby[T](
    key: typing.Any, seq: collections.abc.Iterable[T], /
) -> dict[typing.Any, list[T]]: ...
def groupby[KT, T](
    key: typing.Callable[[T], KT] | typing.Any = ...,
    seq: collections.abc.Iterable[T] = ...,
) -> (
    dict[KT, list[T]]
    | dict[typing.Any, list[T]]
    | typing.Callable[..., dict[KT, list[T]] | dict[typing.Any, list[T]]]
):
    """Curried version of groupby

    Group a collection by a key function.

    >>> from toolz.curried import groupby
    >>> names = ['Alice', 'Bob', 'Charlie', 'Dan', 'Edith', 'Frank']
    >>> groupby(len, names)  # doctest: +SKIP
    {3: ['Bob', 'Dan'], 5: ['Alice', 'Edith', 'Frank'], 7: ['Charlie']}

    Can be partially applied:
    >>> group_by_len = groupby(len)
    >>> group_by_len(names)  # doctest: +SKIP
    {3: ['Bob', 'Dan'], 5: ['Alice', 'Edith', 'Frank'], 7: ['Charlie']}

    Non-callable keys imply grouping on a member:
    >>> groupby('gender', [{'name': 'Alice', 'gender': 'F'},
    ...                    {'name': 'Bob', 'gender': 'M'}])  # doctest: +SKIP
    {'F': [{'gender': 'F', 'name': 'Alice'}],
     'M': [{'gender': 'M', 'name': 'Bob'}]}
    """
    ...

interpose = toolz.curry(toolz.interpose)

@typing.overload
def itemfilter[K, V]() -> typing.Callable[
    ..., dict[K, V] | collections.abc.MutableMapping[K, V]
]: ...

# Stage 1a: Just predicate (no factory) - returns callable waiting for dict
@typing.overload
def itemfilter[K, V](
    predicate: typing.Callable[[tuple[K, V]], bool], /
) -> typing.Callable[[collections.abc.Mapping[K, V]], dict[K, V]]: ...

# Stage 1b: Predicate with factory - returns callable waiting for dict
@typing.overload
def itemfilter[K, V](
    predicate: typing.Callable[[tuple[K, V]], bool],
    /,
    *,
    factory: typing.Callable[[], collections.abc.MutableMapping[K, V]],
) -> typing.Callable[
    [collections.abc.Mapping[K, V]], collections.abc.MutableMapping[K, V]
]: ...

# Stage 2a: Full application (no factory) - executes immediately
@typing.overload
def itemfilter[K, V](
    predicate: typing.Callable[[tuple[K, V]], bool],
    d: collections.abc.Mapping[K, V],
    /,
) -> dict[K, V]: ...

# Stage 2b: Full application (with factory) - executes immediately
@typing.overload
def itemfilter[K, V](
    predicate: typing.Callable[[tuple[K, V]], bool],
    d: collections.abc.Mapping[K, V],
    /,
    *,
    factory: typing.Callable[[], collections.abc.MutableMapping[K, V]],
) -> collections.abc.MutableMapping[K, V]: ...
def itemfilter[K, V](
    predicate: typing.Callable[[tuple[K, V]], bool] = ...,
    d: collections.abc.Mapping[K, V] = ...,
    *,
    factory: typing.Callable[[], collections.abc.MutableMapping[K, V]] = dict,
) -> (
    dict[K, V]
    | collections.abc.MutableMapping[K, V]
    | typing.Callable[..., dict[K, V] | collections.abc.MutableMapping[K, V]]
):
    """Curried version of itemfilter

    Filter items in dictionary by (key, value) tuple.

    >>> from toolz.curried import itemfilter
    >>> def isvalid(item):
    ...     k, v = item
    ...     return k % 2 == 0 and v < 4
    >>> d = {1: 2, 2: 3, 3: 4, 4: 5}
    >>> itemfilter(isvalid, d)
    {2: 3}

    Can be partially applied:
    >>> filter_valid = itemfilter(isvalid)
    >>> filter_valid(d)
    {2: 3}

    Common pattern for filtering by both key and value:
    >>> data = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    >>> itemfilter(lambda item: item[0] < 'c' and item[1] > 1, data)
    {'b': 2}

    See Also:
        keyfilter
        valfilter
        itemmap
    """
    ...

@typing.overload
def itemmap[K0, V0, K1, V1]() -> typing.Callable[
    ..., dict[K1, V1] | collections.abc.MutableMapping[K1, V1]
]: ...

# Stage 1a: Just func (no factory) - returns callable waiting for dict
@typing.overload
def itemmap[K0, V0, K1, V1](
    func: typing.Callable[[tuple[K0, V0]], tuple[K1, V1]], /
) -> typing.Callable[[collections.abc.Mapping[K0, V0]], dict[K1, V1]]: ...

# Stage 1b: Func with factory - returns callable waiting for dict
@typing.overload
def itemmap[K0, V0, K1, V1](
    func: typing.Callable[[tuple[K0, V0]], tuple[K1, V1]],
    /,
    *,
    factory: typing.Callable[[], collections.abc.MutableMapping[K1, V1]],
) -> typing.Callable[
    [collections.abc.Mapping[K0, V0]], collections.abc.MutableMapping[K1, V1]
]: ...

# Stage 2a: Full application (no factory) - executes immediately
@typing.overload
def itemmap[K0, V0, K1, V1](
    func: typing.Callable[[tuple[K0, V0]], tuple[K1, V1]],
    d: collections.abc.Mapping[K0, V0],
    /,
) -> dict[K1, V1]: ...

# Stage 2b: Full application (with factory) - executes immediately
@typing.overload
def itemmap[K0, V0, K1, V1](
    func: typing.Callable[[tuple[K0, V0]], tuple[K1, V1]],
    d: collections.abc.Mapping[K0, V0],
    /,
    *,
    factory: typing.Callable[[], collections.abc.MutableMapping[K1, V1]],
) -> collections.abc.MutableMapping[K1, V1]: ...
def itemmap[K0, V0, K1, V1](
    func: typing.Callable[[tuple[K0, V0]], tuple[K1, V1]] = ...,
    d: collections.abc.Mapping[K0, V0] = ...,
    *,
    factory: typing.Callable[[], collections.abc.MutableMapping[K1, V1]] = dict,
) -> (
    dict[K1, V1]
    | collections.abc.MutableMapping[K1, V1]
    | typing.Callable[..., dict[K1, V1] | collections.abc.MutableMapping[K1, V1]]
):
    """Curried version of itemmap

    Apply function to (key, value) tuples of dictionary.

    >>> from toolz.curried import itemmap
    >>> accountids = {"Alice": 10, "Bob": 20}
    >>> itemmap(reversed, accountids)  # doctest: +SKIP
    {10: "Alice", 20: "Bob"}

    Can be partially applied:
    >>> swap_items = itemmap(reversed)
    >>> swap_items(accountids)  # doctest: +SKIP
    {10: "Alice", 20: "Bob"}

    Common pattern for transforming both keys and values:
    >>> data = {'a': 1, 'b': 2, 'c': 3}
    >>> itemmap(lambda item: (item[0].upper(), item[1] * 10), data)
    {'A': 10, 'B': 20, 'C': 30}

    See Also:
        keymap
        valmap
        itemfilter
    """
    ...

iterate = toolz.curry(toolz.iterate)
join = toolz.curry(toolz.join)

# Curried keyfilter with explicit overloads for type safety
# Stage 0: No arguments - returns a callable
@typing.overload
def keyfilter[K, V]() -> typing.Callable[
    ..., dict[K, V] | collections.abc.MutableMapping[K, V]
]: ...

# Stage 1a: Just predicate (no factory) - returns callable waiting for dict
@typing.overload
def keyfilter[K, V](
    predicate: typing.Callable[[K], bool], /
) -> typing.Callable[[collections.abc.Mapping[K, V]], dict[K, V]]: ...

# Stage 1b: Predicate with factory - returns callable waiting for dict
@typing.overload
def keyfilter[K, V](
    predicate: typing.Callable[[K], bool],
    /,
    *,
    factory: typing.Callable[[], collections.abc.MutableMapping[K, V]],
) -> typing.Callable[
    [collections.abc.Mapping[K, V]], collections.abc.MutableMapping[K, V]
]: ...

# Stage 2a: Full application (no factory) - executes immediately
@typing.overload
def keyfilter[K, V](
    predicate: typing.Callable[[K], bool],
    d: collections.abc.Mapping[K, V],
    /,
) -> dict[K, V]: ...

# Stage 2b: Full application (with factory) - executes immediately
@typing.overload
def keyfilter[K, V](
    predicate: typing.Callable[[K], bool],
    d: collections.abc.Mapping[K, V],
    /,
    *,
    factory: typing.Callable[[], collections.abc.MutableMapping[K, V]],
) -> collections.abc.MutableMapping[K, V]: ...
def keyfilter[K, V](
    predicate: typing.Callable[[K], bool] = ...,
    d: collections.abc.Mapping[K, V] = ...,
    *,
    factory: typing.Callable[[], collections.abc.MutableMapping[K, V]] = dict,
) -> (
    dict[K, V]
    | collections.abc.MutableMapping[K, V]
    | typing.Callable[..., dict[K, V] | collections.abc.MutableMapping[K, V]]
):
    """Curried version of keyfilter

    Filter items in dictionary by key.

    >>> from toolz.curried import keyfilter
    >>> iseven = lambda x: x % 2 == 0
    >>> d = {1: 2, 2: 3, 3: 4, 4: 5}
    >>> keyfilter(iseven, d)
    {2: 3, 4: 5}

    Can be partially applied:
    >>> filter_even_keys = keyfilter(iseven)
    >>> filter_even_keys(d)
    {2: 3, 4: 5}

    Common pattern for filtering dict keys:
    >>> from toolz.curried import pipe
    >>> users = {'admin_alice': 1, 'user_bob': 2, 'admin_charlie': 3}
    >>> keyfilter(lambda k: k.startswith('admin_'), users)
    {'admin_alice': 1, 'admin_charlie': 3}

    See Also:
        valfilter
        itemfilter
        keymap
    """
    ...

@typing.overload
def keymap[K0, K1, V]() -> typing.Callable[
    ..., dict[K1, V] | collections.abc.MutableMapping[K1, V]
]: ...

# Stage 1a: Just func (no factory) - returns callable waiting for dict
@typing.overload
def keymap[K0, K1, V](
    func: typing.Callable[[K0], K1], /
) -> typing.Callable[[collections.abc.Mapping[K0, V]], dict[K1, V]]: ...

# Stage 1b: Func with factory - returns callable waiting for dict
@typing.overload
def keymap[K0, K1, V](
    func: typing.Callable[[K0], K1],
    /,
    *,
    factory: typing.Callable[[], collections.abc.MutableMapping[K1, V]],
) -> typing.Callable[
    [collections.abc.Mapping[K0, V]], collections.abc.MutableMapping[K1, V]
]: ...

# Stage 2a: Full application (no factory) - executes immediately
@typing.overload
def keymap[K0, K1, V](
    func: typing.Callable[[K0], K1],
    d: collections.abc.Mapping[K0, V],
    /,
) -> dict[K1, V]: ...

# Stage 2b: Full application (with factory) - executes immediately
@typing.overload
def keymap[K0, K1, V](
    func: typing.Callable[[K0], K1],
    d: collections.abc.Mapping[K0, V],
    /,
    *,
    factory: typing.Callable[[], collections.abc.MutableMapping[K1, V]],
) -> collections.abc.MutableMapping[K1, V]: ...
def keymap[K0, K1, V](
    func: typing.Callable[[K0], K1] = ...,
    d: collections.abc.Mapping[K0, V] = ...,
    *,
    factory: typing.Callable[[], collections.abc.MutableMapping[K1, V]] = dict,
) -> (
    dict[K1, V]
    | collections.abc.MutableMapping[K1, V]
    | typing.Callable[..., dict[K1, V] | collections.abc.MutableMapping[K1, V]]
):
    """Curried version of keymap

    Apply function to keys of dictionary.

    >>> from toolz.curried import keymap
    >>> bills = {"Alice": [20, 15, 30], "Bob": [10, 35]}
    >>> keymap(str.lower, bills)  # doctest: +SKIP
    {'alice': [20, 15, 30], 'bob': [10, 35]}

    Can be partially applied:
    >>> lowercase_keys = keymap(str.lower)
    >>> lowercase_keys(bills)  # doctest: +SKIP
    {'alice': [20, 15, 30], 'bob': [10, 35]}

    Common pattern for normalizing keys:
    >>> data = {'Name': 'Alice', 'Age': 30, 'City': 'NYC'}
    >>> keymap(str.lower, data)
    {'name': 'Alice', 'age': 30, 'city': 'NYC'}

    See Also:
        valmap
        itemmap
        keyfilter
    """
    ...

@typing.overload
def map[T1, S]() -> typing.Callable[
    ..., collections.abc.Iterator[S] | typing.Callable[..., collections.abc.Iterator[S]]
]: ...
@typing.overload
def map[T1, S](
    func: typing.Callable[[T1], S], /
) -> typing.Callable[[collections.abc.Iterable[T1]], collections.abc.Iterator[S]]: ...
@typing.overload
def map[T1, T2, S](
    func: typing.Callable[[T1, T2], S], /
) -> typing.Callable[
    [collections.abc.Iterable[T1], collections.abc.Iterable[T2]],
    collections.abc.Iterator[S],
]: ...
@typing.overload
def map[T1, T2, T3, S](
    func: typing.Callable[[T1, T2, T3], S], /
) -> typing.Callable[
    [
        collections.abc.Iterable[T1],
        collections.abc.Iterable[T2],
        collections.abc.Iterable[T3],
    ],
    collections.abc.Iterator[S],
]: ...
@typing.overload
def map[T1, T2, T3, T4, S](
    func: typing.Callable[[T1, T2, T3, T4], S], /
) -> typing.Callable[
    [
        collections.abc.Iterable[T1],
        collections.abc.Iterable[T2],
        collections.abc.Iterable[T3],
        collections.abc.Iterable[T4],
    ],
    collections.abc.Iterator[S],
]: ...
@typing.overload
def map[T1, T2, T3, T4, T5, S](
    func: typing.Callable[[T1, T2, T3, T4, T5], S], /
) -> typing.Callable[
    [
        collections.abc.Iterable[T1],
        collections.abc.Iterable[T2],
        collections.abc.Iterable[T3],
        collections.abc.Iterable[T4],
        collections.abc.Iterable[T5],
    ],
    collections.abc.Iterator[S],
]: ...
@typing.overload
def map[T1, S](
    func: typing.Callable[[T1], S], iterable: collections.abc.Iterable[T1], /
) -> collections.abc.Iterator[S]: ...
@typing.overload
def map[T1, T2, S](
    func: typing.Callable[[T1, T2], S],
    iterable: collections.abc.Iterable[T1],
    iter2: collections.abc.Iterable[T2],
    /,
) -> collections.abc.Iterator[S]: ...
@typing.overload
def map[T1, T2, T3, S](
    func: typing.Callable[[T1, T2, T3], S],
    iterable: collections.abc.Iterable[T1],
    iter2: collections.abc.Iterable[T2],
    iter3: collections.abc.Iterable[T3],
    /,
) -> collections.abc.Iterator[S]: ...
@typing.overload
def map[T1, T2, T3, T4, S](
    func: typing.Callable[[T1, T2, T3, T4], S],
    iterable: collections.abc.Iterable[T1],
    iter2: collections.abc.Iterable[T2],
    iter3: collections.abc.Iterable[T3],
    iter4: collections.abc.Iterable[T4],
    /,
) -> collections.abc.Iterator[S]: ...
@typing.overload
def map[T1, T2, T3, T4, T5, S](
    func: typing.Callable[[T1, T2, T3, T4, T5], S],
    iterable: collections.abc.Iterable[T1],
    iter2: collections.abc.Iterable[T2],
    iter3: collections.abc.Iterable[T3],
    iter4: collections.abc.Iterable[T4],
    iter5: collections.abc.Iterable[T5],
    /,
) -> collections.abc.Iterator[S]: ...
@typing.overload
def map[S](
    func: typing.Callable[..., S],
    iterable: collections.abc.Iterable[typing.Any],
    iter2: collections.abc.Iterable[typing.Any],
    iter3: collections.abc.Iterable[typing.Any],
    iter4: collections.abc.Iterable[typing.Any],
    iter5: collections.abc.Iterable[typing.Any],
    iter6: collections.abc.Iterable[typing.Any],
    /,
    *iterables: collections.abc.Iterable[typing.Any],
) -> collections.abc.Iterator[S]: ...
def map[S](
    func: typing.Callable[..., S] = ...,
    *iterables: collections.abc.Iterable[typing.Any],
) -> (
    collections.abc.Iterator[S]
    | typing.Callable[..., collections.abc.Iterator[S]]
    | typing.Callable[
        ...,
        collections.abc.Iterator[S] | typing.Callable[..., collections.abc.Iterator[S]],
    ]
):
    """Curried version of builtin map function

    Apply a function to every element of an iterable(s).

    >>> from toolz.curried import map
    >>> inc = lambda x: x + 1
    >>> list(map(inc, [1, 2, 3]))
    [2, 3, 4]

    Can be partially applied:
    >>> map_inc = map(inc)
    >>> list(map_inc([1, 2, 3]))
    [2, 3, 4]

    Works with multiple iterables:
    >>> add = lambda x, y: x + y
    >>> list(map(add, [1, 2, 3], [10, 20, 30]))
    [11, 22, 33]
    """
    ...

@typing.overload
def mapcat[T, R]() -> typing.Callable[
    ..., collections.abc.Iterator[R] | typing.Callable[..., collections.abc.Iterator[R]]
]: ...
@typing.overload
def mapcat[T, R](
    func: typing.Callable[[collections.abc.Iterable[T]], collections.abc.Iterable[R]], /
) -> typing.Callable[
    [collections.abc.Iterable[collections.abc.Iterable[T]]], collections.abc.Iterator[R]
]: ...
@typing.overload
def mapcat[T, R](
    func: typing.Callable[[collections.abc.Iterable[T]], collections.abc.Iterable[R]],
    seqs: collections.abc.Iterable[collections.abc.Iterable[T]],
    /,
) -> collections.abc.Iterator[R]: ...
def mapcat[T, R](
    func: typing.Callable[
        [collections.abc.Iterable[T]], collections.abc.Iterable[R]
    ] = ...,
    seqs: collections.abc.Iterable[collections.abc.Iterable[T]] = ...,
) -> (
    collections.abc.Iterator[R]
    | typing.Callable[
        [collections.abc.Iterable[collections.abc.Iterable[T]]],
        collections.abc.Iterator[R],
    ]
    | typing.Callable[
        ...,
        collections.abc.Iterator[R] | typing.Callable[..., collections.abc.Iterator[R]],
    ]
):
    """Curried version of mapcat

    Apply func to each sequence in seqs, concatenating results.

    >>> from toolz.curried import mapcat
    >>> list(mapcat(lambda s: [c.upper() for c in s],
    ...             [["a", "b"], ["c", "d", "e"]]))
    ['A', 'B', 'C', 'D', 'E']

    Can be partially applied:
    >>> upper_all = mapcat(lambda s: [c.upper() for c in s])
    >>> list(upper_all([["a", "b"], ["c", "d", "e"]]))
    ['A', 'B', 'C', 'D', 'E']
    """
    ...

nth = toolz.curry(toolz.nth)
partial = toolz.curry(toolz.partial)

@typing.overload
def partition[T]() -> typing.Callable[..., collections.abc.Iterator[tuple[T, ...]]]: ...
@typing.overload
def partition[T](
    n: int, /
) -> typing.Callable[..., collections.abc.Iterator[tuple[T, ...]]]: ...
@typing.overload
def partition[T](
    n: typing.Literal[1], seq: collections.abc.Iterable[T], /
) -> collections.abc.Iterator[tuple[T]]: ...
@typing.overload
def partition[T](
    n: int, seq: collections.abc.Iterable[T], /
) -> collections.abc.Iterator[tuple[T, ...]]: ...
@typing.overload
def partition[T](
    n: typing.Literal[1], seq: collections.abc.Iterable[T], pad: typing.Any, /
) -> collections.abc.Iterator[tuple[T]]:
    # Note: With n=1, tuples always have exactly 1 element, so pad is never used
    ...

@typing.overload
def partition[T, P](
    n: int, seq: collections.abc.Iterable[T], pad: P, /
) -> collections.abc.Iterator[tuple[T | P, ...]]: ...
def partition[T, P](
    n: int = ...,
    seq: collections.abc.Iterable[T] = ...,
    pad: P = ...,
) -> (
    collections.abc.Iterator[tuple[T, ...]]
    | collections.abc.Iterator[tuple[T | P, ...]]
    | typing.Callable[..., collections.abc.Iterator[tuple[T | P, ...]]]
):
    """Curried version of partition

    Partition sequence into tuples of length n.

    >>> from toolz.curried import partition
    >>> list(partition(2, [1, 2, 3, 4]))
    [(1, 2), (3, 4)]

    Can be partially applied:
    >>> partition_pairs = partition(2)
    >>> list(partition_pairs([1, 2, 3, 4]))
    [(1, 2), (3, 4)]

    If length not evenly divisible, final tuple is dropped without pad:
    >>> list(partition(2, [1, 2, 3, 4, 5]))
    [(1, 2), (3, 4)]

    With pad, final tuple is filled:
    >>> list(partition(2, [1, 2, 3, 4, 5], None))
    [(1, 2), (3, 4), (5, None)]

    Common pattern for chunking data:
    >>> from toolz.curried import pipe
    >>> data = range(10)
    >>> list(pipe(data, partition(3)))
    [(0, 1, 2), (3, 4, 5), (6, 7, 8)]

    See Also:
        partition_all
    """
    ...

# Curried partition_all with explicit overloads for type safety
# Stage 0: No arguments - returns a callable
@typing.overload
def partition_all[T]() -> typing.Callable[
    ..., collections.abc.Iterator[tuple[T, ...]]
]: ...

# Stage 1: Just n - returns callable waiting for seq
@typing.overload
def partition_all[T](
    n: typing.Literal[1], /
) -> typing.Callable[
    [collections.abc.Iterable[T]], collections.abc.Iterator[tuple[T]]
]: ...
@typing.overload
def partition_all[T](
    n: int, /
) -> typing.Callable[
    [collections.abc.Iterable[T]], collections.abc.Iterator[tuple[T, ...]]
]: ...

# Stage 2: Full application - executes immediately
@typing.overload
def partition_all[T](
    n: typing.Literal[1], seq: collections.abc.Iterable[T], /
) -> collections.abc.Iterator[tuple[T]]: ...
@typing.overload
def partition_all[T](
    n: int, seq: collections.abc.Iterable[T], /
) -> collections.abc.Iterator[tuple[T, ...]]: ...
def partition_all[T](
    n: int = ..., seq: collections.abc.Iterable[T] = ...
) -> (
    collections.abc.Iterator[tuple[T, ...]]
    | typing.Callable[
        [collections.abc.Iterable[T]],
        collections.abc.Iterator[tuple[T, ...]] | collections.abc.Iterator[tuple[T]],
    ]
    | typing.Callable[..., collections.abc.Iterator[tuple[T, ...]]]
):
    """Curried version of partition_all

    Partition all elements of sequence into tuples of length at most n.

    The final tuple may be shorter to accommodate extra elements.

    >>> from toolz.curried import partition_all
    >>> list(partition_all(2, [1, 2, 3, 4]))
    [(1, 2), (3, 4)]

    >>> list(partition_all(2, [1, 2, 3, 4, 5]))
    [(1, 2), (3, 4), (5,)]

    Can be partially applied:
    >>> partition_pairs = partition_all(2)
    >>> list(partition_pairs([1, 2, 3, 4, 5]))
    [(1, 2), (3, 4), (5,)]

    Common pattern for chunking data:
    >>> from toolz.curried import pipe
    >>> data = range(10)
    >>> list(pipe(data, partition_all(3)))
    [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9,)]

    See Also:
        partition
    """
    ...

partitionby = toolz.curry(toolz.partitionby)
peekn = toolz.curry(toolz.peekn)

@typing.overload
def pluck[T]() -> typing.Callable[
    ..., collections.abc.Iterator[T] | collections.abc.Iterator[tuple[T, ...]]
]: ...
@typing.overload
def pluck[T](
    ind: collections.abc.Sequence[typing.Any], /
) -> (
    typing.Callable[
        [
            collections.abc.Iterable[
                collections.abc.Sequence[T] | collections.abc.Mapping[typing.Any, T]
            ]
        ],
        collections.abc.Iterator[tuple[T, ...]],
    ]
    | typing.Callable[
        [
            collections.abc.Iterable[
                collections.abc.Sequence[T] | collections.abc.Mapping[typing.Any, T]
            ],
            T,
        ],
        collections.abc.Iterator[tuple[T, ...]],
    ]
): ...
@typing.overload
def pluck[T](
    ind: typing.Any, /
) -> (
    typing.Callable[
        [
            collections.abc.Iterable[
                collections.abc.Sequence[T] | collections.abc.Mapping[typing.Any, T]
            ]
        ],
        collections.abc.Iterator[T],
    ]
    | typing.Callable[
        [
            collections.abc.Iterable[
                collections.abc.Sequence[T] | collections.abc.Mapping[typing.Any, T]
            ],
            T,
        ],
        collections.abc.Iterator[T],
    ]
): ...
@typing.overload
def pluck[T](
    ind: collections.abc.Sequence[typing.Any],
    seqs: collections.abc.Iterable[
        collections.abc.Sequence[T] | collections.abc.Mapping[typing.Any, T]
    ],
    /,
) -> collections.abc.Iterator[tuple[T, ...]]: ...
@typing.overload
def pluck[T](
    ind: typing.Any,
    seqs: collections.abc.Iterable[
        collections.abc.Sequence[T] | collections.abc.Mapping[typing.Any, T]
    ],
    /,
) -> collections.abc.Iterator[T]: ...
@typing.overload
def pluck[T](
    ind: collections.abc.Sequence[typing.Any],
    seqs: collections.abc.Iterable[
        collections.abc.Sequence[T] | collections.abc.Mapping[typing.Any, T]
    ],
    default: T,
    /,
) -> collections.abc.Iterator[tuple[T, ...]]: ...
@typing.overload
def pluck[T](
    ind: typing.Any,
    seqs: collections.abc.Iterable[
        collections.abc.Sequence[T] | collections.abc.Mapping[typing.Any, T]
    ],
    default: T,
    /,
) -> collections.abc.Iterator[T]: ...
def pluck[T](
    ind: typing.Any | collections.abc.Sequence[typing.Any] = ...,
    seqs: collections.abc.Iterable[
        collections.abc.Sequence[T] | collections.abc.Mapping[typing.Any, T]
    ] = ...,
    default: T = ...,
) -> (
    collections.abc.Iterator[T]
    | collections.abc.Iterator[tuple[T, ...]]
    | typing.Callable[
        ..., collections.abc.Iterator[T] | collections.abc.Iterator[tuple[T, ...]]
    ]
):
    """Curried version of pluck

    Pluck an element or several elements from each item in a sequence.

    >>> from toolz.curried import pluck
    >>> data = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
    >>> list(pluck('name', data))
    ['Alice', 'Bob']

    Can be partially applied:
    >>> get_names = pluck('name')
    >>> list(get_names(data))
    ['Alice', 'Bob']

    Pluck multiple fields:
    >>> list(pluck(['name', 'age'], data))
    [('Alice', 30), ('Bob', 25)]

    With default for missing keys:
    >>> data_incomplete = [{'name': 'Alice'}, {'name': 'Bob', 'age': 25}]
    >>> list(pluck('age', data_incomplete, default=None))
    [None, 25]

    Common pattern with pipe:
    >>> from toolz.curried import pipe
    >>> users = [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]
    >>> list(pipe(users, pluck('name')))
    ['Alice', 'Bob']

    See Also:
        get
        map
    """
    ...

random_sample = toolz.curry(toolz.random_sample)

@typing.overload
def reduce[T]() -> typing.Callable[..., T]: ...
@typing.overload
def reduce[T](
    function: typing.Callable[[T, T], T], /
) -> typing.Callable[[collections.abc.Iterable[T]], T]: ...
@typing.overload
def reduce[T, S](
    function: typing.Callable[[T, S], T], /
) -> typing.Callable[..., T]: ...
@typing.overload
def reduce[T](
    function: typing.Callable[[T, T], T],
    iterable: collections.abc.Iterable[T],
    /,
) -> T: ...
@typing.overload
def reduce[T, S](
    function: typing.Callable[[T, S], T],
    iterable: collections.abc.Iterable[S],
    initial: T,
    /,
) -> T: ...
def reduce[T, S](
    function: typing.Callable[[T, S], T] = ...,
    iterable: collections.abc.Iterable[S] = ...,
    initial: T = ...,
) -> T | typing.Callable[..., T]:
    """Curried version of functools.reduce

    Apply a function of two arguments cumulatively to items of an iterable,
    reducing it to a single value.

    >>> from toolz.curried import reduce
    >>> from operator import add
    >>> reduce(add, [1, 2, 3, 4])
    10

    Can be partially applied:
    >>> sum_all = reduce(add)
    >>> sum_all([1, 2, 3, 4])
    10

    With initial value:
    >>> reduce(add, [1, 2, 3], 10)
    16
    """
    ...

reduceby = toolz.curry(toolz.reduceby)
remove = toolz.curry(toolz.remove)
sliding_window = toolz.curry(toolz.sliding_window)

# Curried sorted with explicit overloads for type safety
# Note: key and reverse are keyword-only parameters in builtin sorted
# Stage 0: No arguments - returns a callable
@typing.overload
def sorted[T]() -> typing.Callable[..., list[T]]: ...

# Stage 1a: Partial application with keyword args only (no key) - returns callable
@typing.overload
def sorted[T](
    *,
    key: None = None,
    reverse: bool = False,
) -> collections.abc.Callable[[collections.abc.Iterable[T]], list[T]]: ...

# Stage 1b: Partial application with keyword args only (with key) - returns callable
@typing.overload
def sorted[T](
    *,
    key: collections.abc.Callable[[T], _Comparable],
    reverse: bool = False,
) -> collections.abc.Callable[[collections.abc.Iterable[T]], list[T]]: ...

# Stage 2a: Full application (no key) - executes immediately
@typing.overload
def sorted[T](
    iterable: collections.abc.Iterable[T],
    /,
    *,
    key: None = None,
    reverse: bool = False,
) -> list[T]: ...

# Stage 2b: Full application (with key function) - executes immediately
@typing.overload
def sorted[T](
    iterable: collections.abc.Iterable[T],
    /,
    *,
    key: collections.abc.Callable[[T], _Comparable],
    reverse: bool = False,
) -> list[T]: ...

# Implementation signature (catch-all)
def sorted[T](
    iterable: collections.abc.Iterable[T] = ...,
    /,
    *,
    key: collections.abc.Callable[[T], _Comparable] | None = None,
    reverse: bool = False,
) -> list[T] | typing.Callable[..., list[T]]:
    """Curried version of builtin sorted

    Return a new sorted list from the items in iterable.

    >>> from toolz.curried import sorted
    >>> sorted([3, 1, 2])
    [1, 2, 3]

    With key function:
    >>> sorted(['alice', 'Bob', 'Charlie'], key=str.lower)
    ['alice', 'Bob', 'Charlie']

    With reverse:
    >>> sorted([3, 1, 2], reverse=True)
    [3, 2, 1]

    Partial application with keyword args:
    >>> case_insensitive_sort = sorted(key=str.lower)
    >>> case_insensitive_sort(['Bob', 'alice', 'Charlie'])
    ['alice', 'Bob', 'Charlie']

    Common pattern for sorting by attribute:
    >>> users = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
    >>> sorted(users, key=lambda u: u['age'])
    [{'name': 'Bob', 'age': 25}, {'name': 'Alice', 'age': 30}]

    See Also:
        groupby
        unique
    """
    ...

tail = toolz.curry(toolz.tail)

@typing.overload
def take[T]() -> typing.Callable[..., collections.abc.Iterator[T]]: ...
@typing.overload
def take[T](
    n: int, /
) -> typing.Callable[[collections.abc.Iterable[T]], collections.abc.Iterator[T]]: ...
@typing.overload
def take[T](
    n: int, seq: collections.abc.Iterable[T], /
) -> collections.abc.Iterator[T]: ...
def take[T](
    n: int = ..., seq: collections.abc.Iterable[T] = ...
) -> (
    collections.abc.Iterator[T]
    | typing.Callable[[collections.abc.Iterable[T]], collections.abc.Iterator[T]]
    | typing.Callable[..., collections.abc.Iterator[T]]
):
    """Curried version of take

    The first n elements of a sequence.

    >>> from toolz.curried import take
    >>> list(take(2, [10, 20, 30, 40, 50]))
    [10, 20]

    Can be partially applied:
    >>> take_two = take(2)
    >>> list(take_two([10, 20, 30, 40, 50]))
    [10, 20]

    Common pattern with map:
    >>> from toolz.curried import map
    >>> data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    >>> list(map(lambda seq: list(take(2, seq)), data))
    [[1, 2], [4, 5], [7, 8]]

    See Also:
        drop
        tail
    """
    ...

take_nth = toolz.curry(toolz.take_nth)
topk = toolz.curry(toolz.topk)
unique = toolz.curry(toolz.unique)
update_in = toolz.curry(toolz.update_in)

@typing.overload
def valfilter[K, V]() -> typing.Callable[
    ..., dict[K, V] | collections.abc.MutableMapping[K, V]
]: ...

# Stage 1a: Just predicate (no factory) - returns callable waiting for dict
@typing.overload
def valfilter[K, V](
    predicate: typing.Callable[[V], bool], /
) -> typing.Callable[[collections.abc.Mapping[K, V]], dict[K, V]]: ...

# Stage 1b: Predicate with factory - returns callable waiting for dict
@typing.overload
def valfilter[K, V](
    predicate: typing.Callable[[V], bool],
    /,
    *,
    factory: typing.Callable[[], collections.abc.MutableMapping[K, V]],
) -> typing.Callable[
    [collections.abc.Mapping[K, V]], collections.abc.MutableMapping[K, V]
]: ...

# Stage 2a: Full application (no factory) - executes immediately
@typing.overload
def valfilter[K, V](
    predicate: typing.Callable[[V], bool],
    d: collections.abc.Mapping[K, V],
    /,
) -> dict[K, V]: ...

# Stage 2b: Full application (with factory) - executes immediately
@typing.overload
def valfilter[K, V](
    predicate: typing.Callable[[V], bool],
    d: collections.abc.Mapping[K, V],
    /,
    *,
    factory: typing.Callable[[], collections.abc.MutableMapping[K, V]],
) -> collections.abc.MutableMapping[K, V]: ...
def valfilter[K, V](
    predicate: typing.Callable[[V], bool] = ...,
    d: collections.abc.Mapping[K, V] = ...,
    *,
    factory: typing.Callable[[], collections.abc.MutableMapping[K, V]] = dict,
) -> (
    dict[K, V]
    | collections.abc.MutableMapping[K, V]
    | typing.Callable[..., dict[K, V] | collections.abc.MutableMapping[K, V]]
):
    """Curried version of valfilter

    Filter items in dictionary by value.

    >>> from toolz.curried import valfilter
    >>> iseven = lambda x: x % 2 == 0
    >>> d = {1: 2, 2: 3, 3: 4, 4: 5}
    >>> valfilter(iseven, d)
    {1: 2, 3: 4}

    Can be partially applied:
    >>> filter_even_vals = valfilter(iseven)
    >>> filter_even_vals(d)
    {1: 2, 3: 4}

    Common pattern for filtering dict values:
    >>> from toolz.curried import pipe
    >>> scores = {'alice': 85, 'bob': 92, 'charlie': 78, 'diana': 95}
    >>> valfilter(lambda v: v >= 90, scores)
    {'bob': 92, 'diana': 95}

    See Also:
        keyfilter
        itemfilter
        valmap
    """
    ...

@typing.overload
def valmap[K, V0, V1]() -> typing.Callable[
    ..., dict[K, V1] | collections.abc.MutableMapping[K, V1]
]: ...

# Stage 1a: Just func (no factory) - returns callable waiting for dict
@typing.overload
def valmap[K, V0, V1](
    func: typing.Callable[[V0], V1], /
) -> typing.Callable[[collections.abc.Mapping[K, V0]], dict[K, V1]]: ...

# Stage 1b: Func with factory - returns callable waiting for dict
@typing.overload
def valmap[K, V0, V1](
    func: typing.Callable[[V0], V1],
    /,
    *,
    factory: typing.Callable[[], collections.abc.MutableMapping[K, V1]],
) -> typing.Callable[
    [collections.abc.Mapping[K, V0]], collections.abc.MutableMapping[K, V1]
]: ...

# Stage 2a: Full application (no factory) - executes immediately
@typing.overload
def valmap[K, V0, V1](
    func: typing.Callable[[V0], V1],
    d: collections.abc.Mapping[K, V0],
    /,
) -> dict[K, V1]: ...

# Stage 2b: Full application (with factory) - executes immediately
@typing.overload
def valmap[K, V0, V1](
    func: typing.Callable[[V0], V1],
    d: collections.abc.Mapping[K, V0],
    /,
    *,
    factory: typing.Callable[[], collections.abc.MutableMapping[K, V1]],
) -> collections.abc.MutableMapping[K, V1]: ...
def valmap[K, V0, V1](
    func: typing.Callable[[V0], V1] = ...,
    d: collections.abc.Mapping[K, V0] = ...,
    *,
    factory: typing.Callable[[], collections.abc.MutableMapping[K, V1]] = dict,
) -> (
    dict[K, V1]
    | collections.abc.MutableMapping[K, V1]
    | typing.Callable[..., dict[K, V1] | collections.abc.MutableMapping[K, V1]]
):
    """Curried version of valmap

    Apply function to values of dictionary.

    >>> from toolz.curried import valmap
    >>> bills = {"Alice": [20, 15, 30], "Bob": [10, 35]}
    >>> valmap(sum, bills)  # doctest: +SKIP
    {'Alice': 65, 'Bob': 45}

    Can be partially applied:
    >>> sum_values = valmap(sum)
    >>> sum_values(bills)  # doctest: +SKIP
    {'Alice': 65, 'Bob': 45}

    Common pattern for transforming values:
    >>> scores = {'alice': 85, 'bob': 92, 'charlie': 78}
    >>> valmap(lambda x: 'pass' if x >= 80 else 'fail', scores)
    {'alice': 'pass', 'bob': 'pass', 'charlie': 'fail'}

    See Also:
        keymap
        itemmap
        valfilter
    """
    ...
