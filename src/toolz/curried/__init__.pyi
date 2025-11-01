# pyright: reportUnusedImport=false, reportAny=false
# According to PEP561, file structure should mirror the package structure
# That's why this is in curried/__init__.pyi and not just curried.pyi
import collections.abc
import typing

from typing_extensions import TypeIs

import toolz
from toolz import (
    apply,
    comp,
    complement,
    compose,
    compose_left,
    concat,
    concatv,
    count,
    curry,
    diff,
    first,
    flip,
    frequencies,
    identity,
    interleave,
    isdistinct,
    isiterable,
    juxt,
    last,
    memoize,
    merge_sorted,
    peek,
    pipe,
    second,
    thread_first,
    thread_last,
)

# All functions from operator module are re-exported here.
# Binary and n-ary functions are curried; unary functions are not.
# From a typing perspective, curried functions have identical signatures.
from . import operator
from .exceptions import merge, merge_with

accumulate = toolz.curry(toolz.accumulate)
assoc = toolz.curry(toolz.assoc)  # high priority
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

excepts = toolz.curry(toolz.excepts)

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
itemfilter = toolz.curry(toolz.itemfilter)
itemmap = toolz.curry(toolz.itemmap)
iterate = toolz.curry(toolz.iterate)
join = toolz.curry(toolz.join)
keyfilter = toolz.curry(toolz.keyfilter)  # high priority
keymap = toolz.curry(toolz.keymap)  # high priority

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

# Stage 0: No arguments - returns a callable waiting for function
@typing.overload
def mapcat[T, R]() -> typing.Callable[
    ..., collections.abc.Iterator[R] | typing.Callable[..., collections.abc.Iterator[R]]
]: ...

# Stage 1: Just function - returns callable waiting for seqs
@typing.overload
def mapcat[T, R](
    func: typing.Callable[[collections.abc.Iterable[T]], collections.abc.Iterable[R]], /
) -> typing.Callable[
    [collections.abc.Iterable[collections.abc.Iterable[T]]], collections.abc.Iterator[R]
]: ...

# Stage 2: Function + seqs - executes immediately
@typing.overload
def mapcat[T, R](
    func: typing.Callable[[collections.abc.Iterable[T]], collections.abc.Iterable[R]],
    seqs: collections.abc.Iterable[collections.abc.Iterable[T]],
    /,
) -> collections.abc.Iterator[R]: ...

# Implementation signature (catch-all)
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
partition = toolz.curry(toolz.partition)  # high priority
partition_all = toolz.curry(toolz.partition_all)  # high priority
partitionby = toolz.curry(toolz.partitionby)
peekn = toolz.curry(toolz.peekn)
pluck = toolz.curry(toolz.pluck)  # high priority
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
sorted = toolz.curry(toolz.sorted)  # high priority
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
valfilter = toolz.curry(toolz.valfilter)  # high priority
valmap = toolz.curry(toolz.valmap)  # high priority

del toolz
