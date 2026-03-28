# pyright: reportExplicitAny = false
from collections.abc import Callable, Hashable, Mapping, MutableMapping, Sequence
from typing import Any, Literal, overload, Protocol, TypeGuard
import sys
import collections.abc
import typing

if sys.version_info >= (3, 13):
    from typing import TypeIs  # pyright: ignore[reportUnreachable]
else:
    from typing_extensions import TypeIs
__all__ = (
    "assoc",
    "assoc_in",
    "dissoc",
    "get_in",
    "itemfilter",
    "itemmap",
    "keyfilter",
    "keymap",
    "merge",
    "merge_with",
    "update_in",
    "valfilter",
    "valmap",
)

class SupportsGetItem[K: Hashable, V](Protocol):
    def __getitem__(self, key: K, /) -> V: ...

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
) -> MutableMapping[K, V]: ...
@overload
def assoc_in[K1, K2, V1, V2](
    d: Mapping[K1, Mapping[K2, V2] | V1], keys: tuple[K1, K2], value: V2
) -> dict[K1, dict[K2, V2] | V1 | V2]: ...
@overload
def assoc_in[K1, K2, V1, V2](
    d: Mapping[K1, Mapping[K2, V2] | V1],
    keys: tuple[K1, K2],
    value: V2,
    *,
    factory: Callable[[], MutableMapping[K1, Any]],
) -> MutableMapping[K1, Any]: ...
@overload
def assoc_in[K1, K2, K3, V1, V2, V3](
    d: Mapping[K1, Mapping[K2, Mapping[K3, V3] | V2] | V1],
    keys: tuple[K1, K2, K3],
    value: V3,
) -> dict[K1, dict[K2, dict[K3, V3] | V2 | V3] | V1 | V3]: ...
@overload
def assoc_in[K1, K2, K3, V1, V2, V3](
    d: Mapping[K1, Mapping[K2, Mapping[K3, V3] | V2] | V1],
    keys: tuple[K1, K2, K3],
    value: V3,
    *,
    factory: Callable[[], MutableMapping[K1, Any]],
) -> MutableMapping[K1, Any]: ...
@overload
def assoc_in[K, V](d: Mapping[K, V], keys: Sequence[K], value: V) -> dict[K, V]: ...
@overload
def assoc_in[K, V](
    d: Mapping[K, V],
    keys: Sequence[K],
    value: V,
    *,
    factory: Callable[[], MutableMapping[K, V]],
) -> MutableMapping[K, V]: ...
def assoc_in[K, V](
    d: Mapping[K, V],
    keys: Sequence[K],
    value: V,
    *,
    factory: Callable[[], MutableMapping[K, V]] = dict,
) -> MutableMapping[K, V]: ...
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
) -> MutableMapping[K, V]: ...
@overload
def get_in[K: Hashable, V](
    keys: Sequence[K],
    coll: SupportsGetItem[K, V],
    default: None = None,
    no_default: Literal[True] = True,
) -> V: ...
@overload
def get_in[K: Hashable, V](
    keys: Sequence[K],
    coll: SupportsGetItem[K, V],
    default: None = None,
    no_default: bool = False,
) -> V | None: ...
@overload
def get_in[K: Hashable, V](
    keys: Sequence[K], coll: SupportsGetItem[K, V], default: V, no_default: bool = False
) -> V: ...
def get_in[K: Hashable, V](
    keys: Sequence[K],
    coll: SupportsGetItem[K, V],
    default: V | None = None,
    no_default: bool = False,
) -> V | None: ...
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
) -> MutableMapping[K1, V1]: ...
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
) -> MutableMapping[K1, V1]: ...
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
) -> MutableMapping[K1, V]: ...
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
) -> MutableMapping[K1, V]: ...
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
) -> MutableMapping[K, V]: ...
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
) -> MutableMapping[K, V]: ...
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
) -> MutableMapping[K, V1]: ...
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
) -> MutableMapping[K, V1]: ...
