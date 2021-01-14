"""

when get then delete

use it as separate module:

create different view

hierachical dict

Enhanced dict

.filterview()

TreeDict

setting default

"""
from collections.abc import MutableMapping


class MappingDict(MutableMapping):
    def __init__(self, attributes=()):
        self._dict = dict()
        self.update(attributes)

    @property
    def dict(self):
        return self._dict

    def _get(self, field):
        return self._dict[field]

    def __getitem__(self, field):
        return self._get(field=field)

    def _set_field(self, field, value):
        self._dict[field] = value

    def __setitem__(self, field, value):
        self._set_field(field=field, value=value)

    def _delete_field(self, field):
        del self._dict[field]

    def __delitem__(self, field):
        self._delete_field(field=field)

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def __contains__(self, field):
        return field in self._dict


class OrderDict(MappingDict):
    pass


_dict = MappingDict({'a': 1})

print(_dict.get('a'))