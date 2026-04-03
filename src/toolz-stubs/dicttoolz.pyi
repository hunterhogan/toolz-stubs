# pyright: reportExplicitAny = false
from collections.abc import Callable, Hashable, Mapping, MutableMapping, Sequence
from typing import overload, TypeGuard, TypeVar, Protocol, Literal
import sys
import collections.abc
import typing

if sys.version_info >= (3, 13):
    from typing import TypeIs  # pyright: ignore[reportUnreachable]
else:
    from typing_extensions import TypeIs

__all__ = (
    "merge",
    "merge_with",
    "valmap",
    "keymap",
    "itemmap",
    "valfilter",
    "keyfilter",
    "itemfilter",
    "assoc",
    "dissoc",
    "assoc_in",
    "update_in",
    "get_in",
)

@overload
def merge[K: Hashable, V](
    *dicts: Mapping[K, V], factory: Callable[[], dict[K, V]] = dict
) -> dict[K, V]: ...
@overload
def merge[K: Hashable, V](
    *dicts: Mapping[K, V], factory: Callable[[], MutableMapping[K, V]]
) -> MutableMapping[K, V]: ...
def merge[K: Hashable, V](
    *dicts: Mapping[K, V], factory: Callable[[], MutableMapping[K, V]] = dict
) -> MutableMapping[K, V]:
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

@overload
def merge_with[K: Hashable, V](
    func: Callable[[Sequence[V]], V],
    *dicts: Mapping[K, V],
    factory: Callable[[], dict[K, V]] = dict,
) -> dict[K, V]: ...
@overload
def merge_with[K: Hashable, V](
    func: Callable[[Sequence[V]], V],
    *dicts: Mapping[K, V],
    factory: Callable[[], MutableMapping[K, V]],
) -> MutableMapping[K, V]: ...
def merge_with[K: Hashable, V](
    func: Callable[[Sequence[V]], V],
    *dicts: Mapping[K, V],
    factory: Callable[[], MutableMapping[K, V]] = dict,
) -> MutableMapping[K, V]:
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

@overload
def valmap[K: Hashable, V0, V1](
    func: Callable[[V0], V1],
    d: Mapping[K, V0],
    factory: Callable[[], dict[K, V1]] = dict,
) -> dict[K, V1]: ...
@overload
def valmap[K: Hashable, V0, V1](
    func: Callable[[V0], V1],
    d: Mapping[K, V0],
    factory: Callable[[], MutableMapping[K, V1]],
) -> MutableMapping[K, V1]: ...
def valmap[K: Hashable, V0, V1](
    func: Callable[[V0], V1],
    d: Mapping[K, V0],
    factory: Callable[[], MutableMapping[K, V1]] = dict,
) -> MutableMapping[K, V1]:
    """Apply function to values of dictionary

    >>> bills = {"Alice": [20, 15, 30], "Bob": [10, 35]}
    >>> valmap(sum, bills)  # doctest: +SKIP
    {'Alice': 65, 'Bob': 45}

    See Also:
        keymap
        itemmap
    """
    ...

@overload
def keymap[K0: Hashable, K1: Hashable, V](
    func: Callable[[K0], K1],
    d: Mapping[K0, V],
    factory: Callable[[], dict[K1, V]] = dict,
) -> dict[K1, V]: ...
@overload
def keymap[K0: Hashable, K1: Hashable, V](
    func: Callable[[K0], K1],
    d: Mapping[K0, V],
    factory: Callable[[], MutableMapping[K1, V]],
) -> MutableMapping[K1, V]: ...
def keymap[K0: Hashable, K1: Hashable, V](
    func: Callable[[K0], K1],
    d: Mapping[K0, V],
    factory: Callable[[], MutableMapping[K1, V]] = dict,
) -> MutableMapping[K1, V]:
    """Apply function to keys of dictionary

    >>> bills = {"Alice": [20, 15, 30], "Bob": [10, 35]}
    >>> keymap(str.lower, bills)  # doctest: +SKIP
    {'alice': [20, 15, 30], 'bob': [10, 35]}

    See Also:
        valmap
        itemmap
    """
    ...

@overload
def itemmap[K0: Hashable, K1: Hashable, V0, V1](
    func: Callable[[tuple[K0, V0]], tuple[K1, V1]],
    d: Mapping[K0, V0],
    factory: Callable[..., dict[K1, V1]] = dict,
) -> dict[K1, V1]: ...
@overload
def itemmap[K0: Hashable, K1: Hashable, V0, V1](
    func: Callable[[tuple[K0, V0]], tuple[K1, V1]],
    d: Mapping[K0, V0],
    factory: Callable[..., MutableMapping[K1, V1]],
) -> MutableMapping[K1, V1]: ...
def itemmap[K0: Hashable, K1: Hashable, V0, V1](
    func: Callable[[tuple[K0, V0]], tuple[K1, V1]],
    d: Mapping[K0, V0],
    factory: Callable[..., MutableMapping[K1, V1]] = dict,
) -> MutableMapping[K1, V1]:
    """Apply function to items of dictionary

    >>> accountids = {"Alice": 10, "Bob": 20}
    >>> itemmap(reversed, accountids)  # doctest: +SKIP
    {10: "Alice", 20: "Bob"}

    See Also:
        keymap
        valmap
    """
    ...

@overload
def valfilter[K: Hashable, V0, V1](
    predicate: Callable[[V0], TypeIs[V1]],
    d: Mapping[K, V0],
    factory: Callable[[], dict[K, V1]] = dict,
) -> dict[K, V1]: ...
@overload
def valfilter[K: Hashable, V0, V1](
    predicate: Callable[[V0], TypeGuard[V1]],
    d: Mapping[K, V0],
    factory: Callable[[], dict[K, V1]] = dict,
) -> dict[K, V1]: ...
@overload
def valfilter[K: Hashable, V](
    predicate: Callable[[V], bool], d: Mapping[K, V]
) -> dict[K, V]: ...
@overload
def valfilter[K: Hashable, V0, V1](
    predicate: Callable[[V0], TypeIs[V1]],
    d: Mapping[K, V0],
    factory: Callable[[], MutableMapping[K, V1]],
) -> MutableMapping[K, V1]: ...
@overload
def valfilter[K: Hashable, V0, V1](
    predicate: Callable[[V0], TypeGuard[V1]],
    d: Mapping[K, V0],
    factory: Callable[[], MutableMapping[K, V1]],
) -> MutableMapping[K, V1]: ...
@overload
def valfilter[K: Hashable, V0, V1](
    predicate: Callable[[V0], bool],
    d: Mapping[K, V0],
    factory: Callable[[], MutableMapping[K, V1]],
) -> MutableMapping[K, V1]: ...
def valfilter[K: Hashable, V0, V1](
    predicate: Callable[[V0], bool]
    | Callable[[V0], TypeGuard[V1]]
    | Callable[[V0], TypeIs[V1]],
    d: Mapping[K, V0],
    factory: Callable[[], MutableMapping[K, V1]] = dict,
) -> MutableMapping[K, V1]:
    """Filter items in dictionary by value

    >>> iseven = lambda x: x % 2 == 0
    >>> d = {1: 2, 2: 3, 3: 4, 4: 5}
    >>> valfilter(iseven, d)
    {1: 2, 3: 4}

    See Also:
        keyfilter
        itemfilter
        valmap
    """
    ...

@overload
def keyfilter[K0: Hashable, K1: Hashable, V](
    predicate: Callable[[K0], TypeIs[K1]],
    d: Mapping[K0, V],
    factory: Callable[[], dict[K1, V]] = dict,
) -> dict[K1, V]: ...
@overload
def keyfilter[K0: Hashable, K1: Hashable, V](
    predicate: Callable[[K0], TypeGuard[K1]],
    d: Mapping[K0, V],
    factory: Callable[[], dict[K1, V]] = dict,
) -> dict[K1, V]: ...
@overload
def keyfilter[K: Hashable, V](
    predicate: Callable[[K], bool],
    d: Mapping[K, V],
    factory: Callable[[], dict[K, V]] = dict,
) -> dict[K, V]: ...
@overload
def keyfilter[K0: Hashable, K1: Hashable, V](
    predicate: Callable[[K0], TypeIs[K1]],
    d: Mapping[K0, V],
    factory: Callable[[], MutableMapping[K1, V]],
) -> MutableMapping[K1, V]: ...
@overload
def keyfilter[K0: Hashable, K1: Hashable, V](
    predicate: Callable[[K0], TypeGuard[K1]],
    d: Mapping[K0, V],
    factory: Callable[[], MutableMapping[K1, V]],
) -> MutableMapping[K1, V]: ...
@overload
def keyfilter[K0: Hashable, K1: Hashable, V](
    predicate: Callable[[K0], bool],
    d: Mapping[K0, V],
    factory: Callable[[], MutableMapping[K1, V]],
) -> MutableMapping[K1, V]: ...
def keyfilter[K0: Hashable, K1: Hashable, V](
    predicate: Callable[[K0], bool]
    | Callable[[K0], TypeGuard[K1]]
    | Callable[[K0], TypeIs[K1]],
    d: Mapping[K0, V],
    factory: Callable[[], MutableMapping[K1, V]] = dict,
) -> MutableMapping[K1, V]:
    """Filter items in dictionary by key

    >>> iseven = lambda x: x % 2 == 0
    >>> d = {1: 2, 2: 3, 3: 4, 4: 5}
    >>> keyfilter(iseven, d)
    {2: 3, 4: 5}

    See Also:
        valfilter
        itemfilter
        keymap
    """
    ...

@overload
def itemfilter[K0: Hashable, V0, K1: Hashable, V1](
    predicate: Callable[[tuple[K0, V0]], TypeIs[tuple[K1, V1]]],
    d: Mapping[K0, V0],
    factory: Callable[[], dict[K1, V1]] = dict,
) -> dict[K1, V1]: ...
@overload
def itemfilter[K0: Hashable, V0, K1: Hashable, V1](
    predicate: Callable[[tuple[K0, V0]], TypeGuard[tuple[K1, V1]]],
    d: Mapping[K0, V0],
    factory: Callable[[], dict[K1, V1]] = dict,
) -> dict[K1, V1]: ...
@overload
def itemfilter[K: Hashable, V](
    predicate: Callable[[tuple[K, V]], bool],
    d: Mapping[K, V],
    factory: Callable[[], dict[K, V]] = dict,
) -> dict[K, V]: ...
@overload
def itemfilter[K0: Hashable, V0, K1: Hashable, V1](
    predicate: Callable[[tuple[K0, V0]], TypeIs[tuple[K1, V1]]],
    d: Mapping[K0, V0],
    factory: Callable[[], MutableMapping[K1, V1]],
) -> MutableMapping[K1, V1]: ...
@overload
def itemfilter[K0: Hashable, V0, K1: Hashable, V1](
    predicate: Callable[[tuple[K0, V0]], TypeGuard[tuple[K1, V1]]],
    d: Mapping[K0, V0],
    factory: Callable[[], MutableMapping[K1, V1]],
) -> MutableMapping[K1, V1]: ...
@overload
def itemfilter[K0: Hashable, V0, K1: Hashable, V1](
    predicate: Callable[[tuple[K0, V0]], bool],
    d: Mapping[K0, V0],
    factory: Callable[[], MutableMapping[K1, V1]],
) -> MutableMapping[K1, V1]: ...
def itemfilter[K0: Hashable, V0, K1: Hashable, V1](
    predicate: Callable[[tuple[K0, V0]], bool]
    | Callable[[tuple[K0, V0]], TypeGuard[tuple[K1, V1]]]
    | Callable[[tuple[K0, V0]], TypeIs[tuple[K1, V1]]],
    d: Mapping[K0, V0],
    factory: Callable[[], MutableMapping[K1, V1]] = dict,
) -> MutableMapping[K1, V1]:
    """Filter items in dictionary by item

    >>> def isvalid(item):
    ...     k, v = item
    ...     return k % 2 == 0 and v < 4

    >>> d = {1: 2, 2: 3, 3: 4, 4: 5}
    >>> itemfilter(isvalid, d)
    {2: 3}

    See Also:
        keyfilter
        valfilter
        itemmap
    """
    ...

@overload
def assoc[K: Hashable, V](
    d: Mapping[K, V], key: K, value: V, factory: Callable[[], dict[K, V]] = dict
) -> dict[K, V]: ...
@overload
def assoc[K: Hashable, V](
    d: Mapping[K, V], key: K, value: V, factory: Callable[[], MutableMapping[K, V]]
) -> MutableMapping[K, V]: ...
def assoc[K: Hashable, V](
    d: Mapping[K, V],
    key: K,
    value: V,
    factory: Callable[[], MutableMapping[K, V]] = dict,
) -> MutableMapping[K, V]:
    """Return a new dict with new key value pair

    New dict has d[key] set to value. Does not modify the initial dictionary.

    >>> assoc({'x': 1}, 'x', 2)
    {'x': 2}
    >>> assoc({'x': 1}, 'y', 3)   # doctest: +SKIP
    {'x': 1, 'y': 3}
    """
    ...

@overload
def dissoc[K: Hashable, V](
    d: Mapping[K, V], *keys: K, factory: Callable[[], dict[K, V]] = dict
) -> dict[K, V]: ...
@overload
def dissoc[K: Hashable, V](
    d: Mapping[K, V], *keys: K, factory: Callable[[], MutableMapping[K, V]]
) -> MutableMapping[K, V]: ...
def dissoc[K: Hashable, V](
    d: Mapping[K, V], *keys: K, factory: Callable[[], MutableMapping[K, V]] = dict
) -> MutableMapping[K, V]:
    """Return a new dict with the given key(s) removed.

    New dict has d[key] deleted for each supplied key.
    Does not modify the initial dictionary.

    >>> dissoc({'x': 1, 'y': 2}, 'y')
    {'x': 1}
    >>> dissoc({'x': 1, 'y': 2}, 'y', 'x')
    {}
    >>> dissoc({'x': 1}, 'y') # Ignores missing keys
    {'x': 1}
    """
    ...

# Overloads for nested dictionaries with tuple keys (2-level nesting)
@typing.overload
def assoc_in[K1, K2, V1, V2](
    d: collections.abc.Mapping[K1, collections.abc.Mapping[K2, V2] | V1],
    keys: tuple[K1, K2],
    value: V2,
) -> dict[K1, dict[K2, V2] | V1 | V2]: ...
@typing.overload
def assoc_in[K1, K2, V1, V2](
    d: collections.abc.Mapping[K1, collections.abc.Mapping[K2, V2] | V1],
    keys: tuple[K1, K2],
    value: V2,
    *,
    factory: collections.abc.Callable[
        [], collections.abc.MutableMapping[K1, typing.Any]
    ],
) -> collections.abc.MutableMapping[K1, typing.Any]: ...

# Overloads for nested dictionaries with tuple keys (3-level nesting)
@typing.overload
def assoc_in[K1, K2, K3, V1, V2, V3](
    d: collections.abc.Mapping[
        K1, collections.abc.Mapping[K2, collections.abc.Mapping[K3, V3] | V2] | V1
    ],
    keys: tuple[K1, K2, K3],
    value: V3,
) -> dict[K1, dict[K2, dict[K3, V3] | V2 | V3] | V1 | V3]: ...
@typing.overload
def assoc_in[K1, K2, K3, V1, V2, V3](
    d: collections.abc.Mapping[
        K1, collections.abc.Mapping[K2, collections.abc.Mapping[K3, V3] | V2] | V1
    ],
    keys: tuple[K1, K2, K3],
    value: V3,
    *,
    factory: collections.abc.Callable[
        [], collections.abc.MutableMapping[K1, typing.Any]
    ],
) -> collections.abc.MutableMapping[K1, typing.Any]: ...

# General overloads for backwards compatibility
@typing.overload
def assoc_in[K, V](
    d: collections.abc.Mapping[K, V],
    keys: collections.abc.Iterable[K] | K,
    value: V,
) -> dict[K, V]: ...
@typing.overload
def assoc_in[K, V](
    d: collections.abc.Mapping[K, V],
    keys: collections.abc.Iterable[K] | K,
    value: V,
    *,
    factory: collections.abc.Callable[[], collections.abc.MutableMapping[K, V]],
) -> collections.abc.MutableMapping[K, V]: ...
def assoc_in[K, V](
    d: collections.abc.Mapping[K, V],
    keys: collections.abc.Iterable[K] | K,
    value: V,
    *,
    factory: collections.abc.Callable[[], collections.abc.MutableMapping[K, V]] = dict,
) -> collections.abc.MutableMapping[K, V]:
    """Return a new dict with new, potentially nested, key value pair

    >>> purchase = {'name': 'Alice',
    ...             'order': {'items': ['Apple', 'Orange'],
    ...                       'costs': [0.50, 1.25]},
    ...             'credit card': '5555-1234-1234-1234'}
    >>> assoc_in(purchase, ['order', 'costs'], [0.25, 1.00]) # doctest: +SKIP
    {'credit card': '5555-1234-1234-1234',
     'name': 'Alice',
     'order': {'costs': [0.25, 1.00], 'items': ['Apple', 'Orange']}}
    """
    ...

@typing.overload
def update_in[K, V](
    d: collections.abc.Mapping[K, V],
    keys: collections.abc.Iterable[K] | K,
    func: collections.abc.Callable[..., V],
    default: typing.Any | None = None,
) -> dict[K, V]: ...
@typing.overload
def update_in[K, V](
    d: collections.abc.Mapping[K, V],
    keys: collections.abc.Iterable[K] | K,
    func: collections.abc.Callable[..., V],
    default: typing.Any | None,
    factory: collections.abc.Callable[[], collections.abc.MutableMapping[K, V]],
) -> collections.abc.MutableMapping[K, V]: ...
@typing.overload
def update_in[K, V](
    d: collections.abc.Mapping[K, V],
    keys: collections.abc.Iterable[K] | K,
    func: collections.abc.Callable[..., V],
    default: typing.Any | None = None,
    factory: collections.abc.Callable[[], collections.abc.MutableMapping[K, V]] = dict,
) -> collections.abc.MutableMapping[K, V]: ...
def update_in[K, V](
    d: collections.abc.Mapping[K, V],
    keys: collections.abc.Iterable[K] | K,
    func: collections.abc.Callable[..., V],
    default: typing.Any | None = None,
    factory: collections.abc.Callable[[], collections.abc.MutableMapping[K, V]] = dict,
) -> collections.abc.MutableMapping[K, V]:
    """Update value in a (potentially) nested dictionary

    inputs:
    d - dictionary on which to operate
    keys - list or tuple giving the location of the value to be changed in d
    func - function to operate on that value

    If keys == [k0,..,kX] and d[k0]..[kX] == v, update_in returns a copy of the
    original dictionary with v replaced by func(v), but does not mutate the
    original dictionary.

    If k0 is not a key in d, update_in creates nested dictionaries to the depth
    specified by the keys, with the innermost value set to func(default).

    >>> inc = lambda x: x + 1
    >>> update_in({'a': 0}, ['a'], inc)
    {'a': 1}

    >>> transaction = {'name': 'Alice',
    ...                'purchase': {'items': ['Apple', 'Orange'],
    ...                             'costs': [0.50, 1.25]},
    ...                'credit card': '5555-1234-1234-1234'}
    >>> update_in(transaction, ['purchase', 'costs'], sum) # doctest: +SKIP
    {'credit card': '5555-1234-1234-1234',
     'name': 'Alice',
     'purchase': {'costs': 1.75, 'items': ['Apple', 'Orange']}}

    >>> # updating a value when k0 is not in d
    >>> update_in({}, [1, 2, 3], str, default="bar")
    {1: {2: {3: 'bar'}}}
    >>> update_in({1: 'foo'}, [2, 3, 4], inc, 0)
    {1: 'foo', 2: {3: {4: 1}}}
    """
    ...

_KT_contra = TypeVar("_KT_contra", contravariant=True)
_VT_co = TypeVar("_VT_co", covariant=True)

class _SupportsGetItem(Protocol[_KT_contra, _VT_co]):
    def __getitem__(self, key: _KT_contra, /) -> _VT_co: ...

@typing.overload
def get_in[K, V](
    keys: collections.abc.Sequence[K],
    coll: collections.abc.Sequence[V] | _SupportsGetItem[K, V],
    default: None = None,
    *,
    no_default: Literal[True] = True,
) -> V: ...
@typing.overload
def get_in[K, V](
    keys: collections.abc.Sequence[K],
    coll: collections.abc.Sequence[V] | _SupportsGetItem[K, V],
    default: V,
    no_default: Literal[True] = True,
) -> V: ...
@typing.overload
def get_in[K, V0, V1](
    keys: collections.abc.Sequence[K],
    coll: collections.abc.Sequence[V0] | _SupportsGetItem[K, V0],
    default: V1,
    no_default: bool = False,
) -> V0 | V1: ...
@typing.overload
def get_in[K, V](
    keys: collections.abc.Sequence[K],
    coll: collections.abc.Sequence[V] | _SupportsGetItem[K, V],
    default: None = None,
    no_default: bool = False,
) -> V | None: ...
def get_in[K, V0, V1](
    keys: collections.abc.Sequence[K],
    coll: collections.abc.Sequence[V0] | _SupportsGetItem[K, V0],
    default: V1 | None = None,
    no_default: bool = False,
) -> V0 | V1 | None:
    """Returns coll[i0][i1]...[iX] where [i0, i1, ..., iX]==keys.

    If coll[i0][i1]...[iX] cannot be found, returns ``default``, unless
    ``no_default`` is specified, then it raises KeyError or IndexError.

    ``get_in`` is a generalization of ``operator.getitem`` for nested data
    structures such as dictionaries and lists.

    >>> transaction = {'name': 'Alice',
    ...                'purchase': {'items': ['Apple', 'Orange'],
    ...                             'costs': [0.50, 1.25]},
    ...                'credit card': '5555-1234-1234-1234'}
    >>> get_in(['purchase', 'items', 0], transaction)
    'Apple'
    >>> get_in(['name'], transaction)
    'Alice'
    >>> get_in(['purchase', 'total'], transaction)
    >>> get_in(['purchase', 'items', 'apple'], transaction)
    >>> get_in(['purchase', 'items', 10], transaction)
    >>> get_in(['purchase', 'total'], transaction, 0)
    0
    >>> get_in(['y'], {}, no_default=True)
    Traceback (most recent call last):
        ...
    KeyError: 'y'

    See Also:
        itertoolz.get
        operator.getitem
    """
    ...
