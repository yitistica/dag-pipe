from collections.abc import MutableMapping


class ObjectAttributeOccupiedError(Exception):  # TEMP
    def __init__(self, field):
        message = f'field name <{field}> is already used as an attribute of the object.'
        super().__init__(message)


class ImmutableFieldError(Exception):  # TEMP
    def __init__(self, field):
        message = f'field name <{field}> is not mutable after instantiation.'
        super().__init__(message)


class NullFieldError(Exception):  # TEMP
    def __init__(self, field):
        message = f'field name <{field}> is not null.'
        super().__init__(message)


class AttributeBase(MutableMapping):
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


class GetAttrMixin(object):
    def __getattr__(self, field):
        return self._get_field(field)


class ImmutableFieldMixin(object):
    def __init__(self, fields):
        self._immutable_fields = fields

    @property
    def immutable_fields(self):
        return self._immutable_fields

    def _check_immutable(self, field):
        if (field in self._immutable_fields) and (field in self.attris):
            raise ImmutableFieldError(field)


class NotNullFieldMixin(object):
    def __init__(self, fields):
        if not fields:
            fields = list()
        self._not_null_fields = fields

    @property
    def immutable_fields(self):
        return self._not_null_fields

    def _check_null(self, field):
        if (field in self._not_null_fields) and (field in self.attris):
            raise NullFieldError(field)


class Attributes(AttributeBase, GetAttrMixin, ImmutableFieldMixin):
    def __init__(self, attributes=(), immutable_fields=None):
        ImmutableFieldMixin.__init__(self, fields=immutable_fields)
        AttributeBase.__init__(self, attributes=attributes)

    def _set_field(self, field, value):
        self._check_immutable(field)
        AttributeBase._set_field(self, field, value)
