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


