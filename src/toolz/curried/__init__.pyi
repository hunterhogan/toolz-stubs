# pyright: reportUnusedImport=false
# According to PEP561, file structure should mirror the package structure
# That's why this is in curried/__init__.pyi and not just curried.pyi
import collections.abc
import typing

from typing_extensions import TypeIs

import toolz
from toolz import (  # noqa: F401
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

accumulate = toolz.curry(toolz.accumulate)
assoc = toolz.curry(toolz.assoc)
assoc_in = toolz.curry(toolz.assoc_in)
cons = toolz.curry(toolz.cons)
countby = toolz.curry(toolz.countby)
dissoc = toolz.curry(toolz.dissoc)
do = toolz.curry(toolz.do)
drop = toolz.curry(toolz.drop)
excepts = toolz.curry(toolz.excepts)

# Curried filter with explicit overloads for type safety
# Stage 0: No arguments - returns a callable waiting for predicate
@typing.overload
def filter[T]() -> typing.Callable[
    ..., collections.abc.Iterator[T] | typing.Callable[..., collections.abc.Iterator[T]]
]: ...

# Stage 1: Just predicate (None) - returns callable waiting for iterable
@typing.overload
def filter[T](
    function: None, /
) -> typing.Callable[
    [collections.abc.Iterable[T | None]], collections.abc.Iterator[T]
]: ...

# Stage 1: Just predicate (TypeGuard) - returns callable waiting for iterable
@typing.overload
def filter[S, T](
    function: typing.Callable[[S], typing.TypeGuard[T]], /
) -> typing.Callable[[collections.abc.Iterable[S]], collections.abc.Iterator[T]]: ...

# Stage 1: Just predicate (TypeIs) - returns callable waiting for iterable
@typing.overload
def filter[S, T](
    function: typing.Callable[[S], TypeIs[T]], /
) -> typing.Callable[[collections.abc.Iterable[S]], collections.abc.Iterator[T]]: ...

# Stage 1: Just predicate (regular callable) - returns callable waiting for iterable
@typing.overload
def filter[T](
    function: typing.Callable[[T], typing.Any], /
) -> typing.Callable[[collections.abc.Iterable[T]], collections.abc.Iterator[T]]: ...

# Stage 2: None predicate + iterable - executes immediately, filters out falsy values
@typing.overload
def filter[T](
    function: None, iterable: collections.abc.Iterable[T | None], /
) -> collections.abc.Iterator[T]: ...

# Stage 2: TypeGuard predicate + iterable - executes immediately with type narrowing
@typing.overload
def filter[S, T](
    function: typing.Callable[[S], typing.TypeGuard[T]],
    iterable: collections.abc.Iterable[S],
    /,
) -> collections.abc.Iterator[T]: ...

# Stage 2: TypeIs predicate + iterable - executes immediately with type narrowing
@typing.overload
def filter[S, T](
    function: typing.Callable[[S], TypeIs[T]],
    iterable: collections.abc.Iterable[S],
    /,
) -> collections.abc.Iterator[T]: ...

# Stage 2: Regular callable + iterable - executes immediately
@typing.overload
def filter[T](
    function: typing.Callable[[T], typing.Any],
    iterable: collections.abc.Iterable[T],
    /,
) -> collections.abc.Iterator[T]: ...

# Implementation signature (catch-all)
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

get = toolz.curry(toolz.get)
get_in = toolz.curry(toolz.get_in)

# Curried groupby with explicit overloads for type safety
# Stage 0: No arguments
@typing.overload
def groupby[KT, T]() -> typing.Callable[..., dict[KT, list[T]]]: ...

# Stage 1: Just key function - returns callable waiting for seq
@typing.overload
def groupby[KT, T](
    key: typing.Callable[[T], KT], /
) -> typing.Callable[[collections.abc.Iterable[T]], dict[KT, list[T]]]: ...

# Stage 1: Just key (non-callable, like string) - returns callable waiting for seq
# When key is not callable, it's used with getter to extract attribute/key
@typing.overload
def groupby[T](
    key: typing.Any, /
) -> typing.Callable[[collections.abc.Iterable[T]], dict[typing.Any, list[T]]]: ...

# Stage 2: Key function + seq - executes immediately
@typing.overload
def groupby[KT, T](
    key: typing.Callable[[T], KT], seq: collections.abc.Iterable[T], /
) -> dict[KT, list[T]]: ...

# Stage 2: Non-callable key + seq - executes immediately
@typing.overload
def groupby[T](
    key: typing.Any, seq: collections.abc.Iterable[T], /
) -> dict[typing.Any, list[T]]: ...

# Implementation signature (catch-all)
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
keyfilter = toolz.curry(toolz.keyfilter)
keymap = toolz.curry(toolz.keymap)

# Curried map with explicit overloads for type safety
# Stage 0: No arguments - returns a callable waiting for function
@typing.overload
def map[T1, S]() -> typing.Callable[
    ..., collections.abc.Iterator[S] | typing.Callable[..., collections.abc.Iterator[S]]
]: ...

# Stage 1: Just function, single iterable case - returns callable waiting for 1+ iterables
@typing.overload
def map[T1, S](
    func: typing.Callable[[T1], S], /
) -> typing.Callable[[collections.abc.Iterable[T1]], collections.abc.Iterator[S]]: ...

# Stage 1: Just function, 2 iterables case
@typing.overload
def map[T1, T2, S](
    func: typing.Callable[[T1, T2], S], /
) -> typing.Callable[
    [collections.abc.Iterable[T1], collections.abc.Iterable[T2]],
    collections.abc.Iterator[S],
]: ...

# Stage 1: Just function, 3 iterables case
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

# Stage 1: Just function, 4 iterables case
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

# Stage 1: Just function, 5 iterables case
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

# Stage 2: Function + 1 iterable - executes immediately
@typing.overload
def map[T1, S](
    func: typing.Callable[[T1], S], iterable: collections.abc.Iterable[T1], /
) -> collections.abc.Iterator[S]: ...

# Stage 2: Function + 2 iterables - executes immediately
@typing.overload
def map[T1, T2, S](
    func: typing.Callable[[T1, T2], S],
    iterable: collections.abc.Iterable[T1],
    iter2: collections.abc.Iterable[T2],
    /,
) -> collections.abc.Iterator[S]: ...

# Stage 2: Function + 3 iterables - executes immediately
@typing.overload
def map[T1, T2, T3, S](
    func: typing.Callable[[T1, T2, T3], S],
    iterable: collections.abc.Iterable[T1],
    iter2: collections.abc.Iterable[T2],
    iter3: collections.abc.Iterable[T3],
    /,
) -> collections.abc.Iterator[S]: ...

# Stage 2: Function + 4 iterables - executes immediately
@typing.overload
def map[T1, T2, T3, T4, S](
    func: typing.Callable[[T1, T2, T3, T4], S],
    iterable: collections.abc.Iterable[T1],
    iter2: collections.abc.Iterable[T2],
    iter3: collections.abc.Iterable[T3],
    iter4: collections.abc.Iterable[T4],
    /,
) -> collections.abc.Iterator[S]: ...

# Stage 2: Function + 5 iterables - executes immediately
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

# Variadic case: 6+ iterables
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

# Implementation signature (catch-all)
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
partition = toolz.curry(toolz.partition)
partition_all = toolz.curry(toolz.partition_all)
partitionby = toolz.curry(toolz.partitionby)
peekn = toolz.curry(toolz.peekn)
pluck = toolz.curry(toolz.pluck)
random_sample = toolz.curry(toolz.random_sample)

# Curried reduce with explicit overloads for type safety
# Stage 0: No arguments
@typing.overload
def reduce[T]() -> typing.Callable[..., T]: ...

# Stage 1: Just function (without initial value) - elements and accumulator same type
@typing.overload
def reduce[T](
    function: typing.Callable[[T, T], T], /
) -> typing.Callable[[collections.abc.Iterable[T]], T]: ...

# Stage 1: Just function (with initial value support) - different types possible
@typing.overload
def reduce[T, S](
    function: typing.Callable[[T, S], T], /
) -> typing.Callable[..., T]: ...

# Stage 2: Function + iterable (without initial) - executes immediately
@typing.overload
def reduce[T](
    function: typing.Callable[[T, T], T],
    iterable: collections.abc.Iterable[T],
    /,
) -> T: ...

# Stage 2: Function + iterable + initial - executes immediately
@typing.overload
def reduce[T, S](
    function: typing.Callable[[T, S], T],
    iterable: collections.abc.Iterable[S],
    initial: T,
    /,
) -> T: ...

# Implementation signature (catch-all)
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
sorted = toolz.curry(toolz.sorted)
tail = toolz.curry(toolz.tail)
take = toolz.curry(toolz.take)
take_nth = toolz.curry(toolz.take_nth)
topk = toolz.curry(toolz.topk)
unique = toolz.curry(toolz.unique)
update_in = toolz.curry(toolz.update_in)
valfilter = toolz.curry(toolz.valfilter)
valmap = toolz.curry(toolz.valmap)

@typing.overload
def merge_with[K, V]() -> typing.Callable[
    ..., dict[K, V] | collections.abc.MutableMapping[K, V]
]: ...
@typing.overload
def merge_with[K, V](
    func: typing.Callable[[collections.abc.Iterable[V]], V], /
) -> typing.Callable[..., dict[K, V] | collections.abc.MutableMapping[K, V]]: ...
@typing.overload
def merge_with[K, V](
    func: typing.Callable[[collections.abc.Iterable[V]], V],
    d: collections.abc.Mapping[K, V],
    /,
) -> dict[K, V]: ...
@typing.overload
def merge_with[K, V](
    func: typing.Callable[[collections.abc.Iterable[V]], V],
    d: collections.abc.Mapping[K, V],
    d2: collections.abc.Mapping[K, V],
    /,
    *dicts: collections.abc.Mapping[K, V],
) -> dict[K, V]: ...
@typing.overload
def merge_with[K, V](
    func: typing.Callable[[collections.abc.Iterable[V]], V],
    d: collections.abc.Mapping[K, V],
    d2: collections.abc.Mapping[K, V],
    /,
    *dicts: collections.abc.Mapping[K, V],
    factory: typing.Callable[[], collections.abc.MutableMapping[K, V]],
) -> collections.abc.MutableMapping[K, V]: ...
@typing.overload
def merge_with[K, V](
    func: typing.Callable[[collections.abc.Iterable[V]], V],
    /,
    *,
    factory: typing.Callable[[], collections.abc.MutableMapping[K, V]],
) -> typing.Callable[..., collections.abc.MutableMapping[K, V]]: ...
def merge_with[K, V](
    func: typing.Callable[[collections.abc.Iterable[V]], V] = ...,
    d: collections.abc.Mapping[K, V] = ...,
    *dicts: collections.abc.Mapping[K, V],
    factory: typing.Callable[[], collections.abc.MutableMapping[K, V]] = ...,
) -> (
    dict[K, V]
    | collections.abc.MutableMapping[K, V]
    | typing.Callable[..., dict[K, V] | collections.abc.MutableMapping[K, V]]
):
    """Merge dictionaries and apply function to combined values

    A key may occur in more than one dict, and all values mapped from the key
    will be passed to the function as a list, such as func([val1, val2, ...]).

    >>> merge_with(sum, {1: 1, 2: 2}, {1: 10, 2: 20})
    {1: 11, 2: 22}

    >>> merge_with(first, {1: 1, 2: 2}, {2: 20, 3: 30})  # doctest: +SKIP
    {1: 1, 2: 2, 3: 30}

    See Also:
        merge
    """
    ...

@typing.overload
def merge[K, V]() -> typing.Callable[
    ..., dict[K, V] | collections.abc.MutableMapping[K, V]
]: ...
@typing.overload
def merge[K, V](d: collections.abc.Mapping[K, V], /) -> dict[K, V]: ...
@typing.overload
def merge[K, V](
    d: collections.abc.Mapping[K, V],
    d2: collections.abc.Mapping[K, V],
    /,
    *dicts: collections.abc.Mapping[K, V],
) -> dict[K, V]: ...
@typing.overload
def merge[K, V](
    d: collections.abc.Mapping[K, V],
    d2: collections.abc.Mapping[K, V],
    /,
    *dicts: collections.abc.Mapping[K, V],
    factory: typing.Callable[[], collections.abc.MutableMapping[K, V]],
) -> collections.abc.MutableMapping[K, V]: ...
@typing.overload
def merge[K, V](
    *,
    factory: typing.Callable[[], collections.abc.MutableMapping[K, V]],
) -> typing.Callable[..., collections.abc.MutableMapping[K, V]]: ...
def merge[K, V](
    d: collections.abc.Mapping[K, V] = ...,
    *dicts: collections.abc.Mapping[K, V],
    factory: typing.Callable[[], collections.abc.MutableMapping[K, V]] = ...,
) -> (
    dict[K, V]
    | collections.abc.MutableMapping[K, V]
    | typing.Callable[..., dict[K, V] | collections.abc.MutableMapping[K, V]]
):
    """Merge a collection of dictionaries

    >>> merge({1: 'one'}, {2: 'two'})
    {1: 'one', 2: 'two'}

    Later dictionaries have precedence

    >>> merge({1: 2, 3: 4}, {3: 3, 4: 4})
    {1: 2, 3: 3, 4: 4}

    See Also:
        merge_with
    """
    ...
