from dag_pipe.helpers.elemental.element import Element
from dag_pipe.helpers.elemental.attributes import Attributes


_PLACEHOLDER_VAR_NAME = 'place_holder'


class AnyValue(object):
    pass


class PlaceHolder(Element):
    def __init__(self, attribute_dict=None, validators=None):
        value = AnyValue

        if attribute_dict is None:
            attribute_dict = dict()

        attribute_dict = {_PLACEHOLDER_VAR_NAME: True, **attribute_dict}
        attributes = Attributes(attributes=attribute_dict, immutable_fields=[])
        super().__init__(value=value, attributes=attributes, validators=validators)

    def set_value(self, value):
        self.validate(value=value)
        del self.attributes[_PLACEHOLDER_VAR_NAME]
        super().__init__(value=value, attributes=self.attributes, validators=self.validator_set.validators)

