"""

when get then delete

use it as separate module:

create different view

hierachical dict

Enhanced dict

.filterview()

TreeDict

setting default

where condition , mixin
"""
from collections.abc import MutableMapping
from dag_pipe.utils.types import check_is_ordered_sequence
from dag_pipe.utils.types import check_container_class

_KEY_ITERABLE_TYPE = [dict]
_CONTAINER_ITERABLE_TYPE = [list, tuple, set]


class MappingDict(MutableMapping):
    def __init__(self, iterable=()):
        self._dict = dict()
        self.update(iterable)

    @property
    def dict(self):
        return self._dict

    def _get(self, key):
        return self._dict[key]

    def __getitem__(self, key):
        return self._get(key=key)

    def _set(self, key, value):
        self._dict[key] = value

    def __setitem__(self, key, value):
        self._set(key=key, value=value)

    def _delete(self, key):
        del self._dict[key]

    def __delitem__(self, key):
        self._delete(key=key)

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def __contains__(self, key):
        return key in self._dict


class ValueCollection(object):
    def __new__(cls, collection):
        if check_is_ordered_sequence(collection):
            self = super().__new__(cls)
        else:
            raise TypeError(f"collection takes only an iterable, but was given an {type(collection)}")
        return self

    def __init__(self, collection):
        self.collection = list(collection)  # turn into list

    def __iter__(self):
        return ValueCollectionIterator(self)

    def __repr__(self):
        if hasattr(self.collection, '__repr__'):
            return f"ValueCollection({self.collection.__repr__()})"
        else:
            return None

    def __str__(self):
        if hasattr(self.collection, '__str__'):
            return f"ValueCollection({self.collection.__str__()})"
        else:
            return None

    def append(self, value):
        self.collection.append(value)

    def remove(self, index):
        del self.collection[index]


class ValueCollectionIterator(object):
    def __new__(cls, value_collection):
        if isinstance(value_collection, ValueCollection):
            self = super().__new__(cls)
        else:
            raise TypeError(f"value_collection arg does not support the type: {type(value_collection)}")
        return self

    def __init__(self, value_collection):
        self.value_collection = value_collection
        self._type = check_container_class(value_collection.collection)
        self._collection_iterator = None
        self._build_collection_iterator()

    def _build_collection_iterator(self):
        if self._type in (_KEY_ITERABLE_TYPE + _CONTAINER_ITERABLE_TYPE):
            self._collection_iterator = iter(self.value_collection.collection)
        else:
            raise TypeError(f'type {self._type} is not supported.')

    def __next__(self):
        _next = next(self._collection_iterator)
        if self._type in _KEY_ITERABLE_TYPE:
            return self.value_collection.collection[_next]
        elif self._type in _CONTAINER_ITERABLE_TYPE:
            return _next
        else:
            raise TypeError(f'type {self._type} is not supported.')

