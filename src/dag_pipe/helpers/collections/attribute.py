"""

set default


validate:

enforce:


"""
from collections.abc import MutableMapping


class ObjectAttributeOccupiedError(Exception):  # TEMP
    def __init__(self, field):
        message = f'field name <{field}> is already used as an attribute of the object.'
        super().__init__(message)


class ImmutableFieldError(Exception):  # TEMP
    def __init__(self, field):
        message = f'field name <{field}> is not mutable after instantiation.'
        super().__init__(message)


class Attribute(MutableMapping):
    def __init__(self, attributes=()):
        self._attris = dict()
        self.update(attributes)

    @property
    def attris(self):
        return self._attris

    def _get_field(self, field):
        return self._attris[field]

    def __getitem__(self, field):
        return self._get_field(field=field)

    def _set_field(self, field, value):
        self._attris[field] = value

    def __setitem__(self, field, value):
        self._set_field(field=field, value=value)

    def _delete_field(self, field):
        del self._attris[field]

    def __delitem__(self, field):
        self._delete_field(field=field)

    def __iter__(self):
        return iter(self._attris)

    def __len__(self):
        return len(self._attris)


class ImmutableFieldMixin(object):
    def __init__(self, fields):
        self._immutable_fields = fields

    def _check_field(self, field, value):
        if (field in self._immutable_fields) and (field in self.attris):
            raise ImmutableFieldError(field)
        else:
            pass


class GetAttrMixin(object):
    def __getattr__(self, field):
        if hasattr(self, field):
            raise ObjectAttributeOccupiedError(field=field)

        return self[field]


class SuperAttribute(ImmutableFieldMixin, Attribute):
    def __init__(self, attributes=(), immutable_fields=None):
        ImmutableFieldMixin.__init__(self, fields=immutable_fields)
        Attribute.__init__(self, attributes=attributes)


if __name__ == '__main__':
    attr = SuperAttribute({'a': 1, 'b': 2}, immutable_fields=['a'])
    attr['a'] = 2


