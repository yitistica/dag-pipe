from dag_pipe.helpers.elemental.element import Element
from dag_pipe.helpers.elemental.attributes import Attributes
from dag_pipe.compartment.validators import check_type


_PLACEHOLDER_VAR_NAME = 'place_holder'
_PARAM_VAR_NAME = 'param'


class AnyValue(object):
    pass


class EmptyValue(object):
    pass


class Feed(Element):
    def __init__(self, value, **attributes):
        attributes = Attributes(attributes)
        super().__init__(value=value, attributes=attributes)


class PlaceHolder(Feed):
    def __init__(self, **attributes):
        value = AnyValue

        attributes = {_PLACEHOLDER_VAR_NAME: True, **attributes}
        super().__init__(value=value, **attributes)

    def set_value(self, value):
        self.validate(value=value)
        del self.attributes[_PLACEHOLDER_VAR_NAME]
        super().__init__(value=value, attributes=self.attributes, validators=self.validator_set.validators)

