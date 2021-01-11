from dag_pipe.helpers.elemental.element import Element
from dag_pipe.helpers.elemental.attributes import Attributes


_FEED_TYPE_FIELD_NAME = '_type'
_FEED_TYPE_VALUE_DEFAULT = 'feed'
_FEED_TYPE_VALUE_PLACEHOLDER = 'placeholder'
_FEED_TYPE_VALUE_PARAM = 'param'

_PARAM_VALUE_TYPE_VAR_NAME = 'value_type'


class AnyValue(object):
    pass


class EmptyValue(object):
    pass


class Feed(Element):
    def __init__(self, value, **attributes):

        if _FEED_TYPE_FIELD_NAME not in attributes:
            attributes = {_FEED_TYPE_FIELD_NAME: _FEED_TYPE_VALUE_DEFAULT, **attributes}

        attributes = Attributes(attributes)
        super().__init__(value=value, attributes=attributes)

    @property
    def type(self):
        return self.attributes[_FEED_TYPE_FIELD_NAME]


class PlaceHolder(Feed):
    def __init__(self, **attributes):
        value = AnyValue

        attributes = {_FEED_TYPE_FIELD_NAME: _FEED_TYPE_VALUE_PLACEHOLDER, **attributes}
        super().__init__(value=value, **attributes)

    def set_value(self, value):
        self.validate(value=value)
        self.set_value(value=value)


class Param(Feed):
    def __init__(self, value, **attributes):

        attributes = {_FEED_TYPE_FIELD_NAME: _FEED_TYPE_VALUE_PARAM, **attributes}
        attributes = Attributes(attributes)

        super().__init__(value=value, attributes=attributes)

        if _PARAM_VALUE_TYPE_VAR_NAME in self.attributes:
            pass  # TODO: add validator
