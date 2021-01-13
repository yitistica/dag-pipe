from dag_pipe.helpers.elemental.element import Element
from dag_pipe.helpers.elemental.attributes import Attributes
from dag_pipe.compartment.validators import BasicTypeValidator


feed_type_value_placeholder = 'placeholder'
feed_type_value_param = 'param'

# data types:
_DATA_TYPE_FIELD_NAME = 'data_type'
_DATA_TYPE_VALUE_CONFIG = 'config'


class AnyValue(object):
    pass


class EmptyValue(object):
    pass


class Feed(Element):
    _meta_dict = {'type': 'feed'}
    meta = Attributes(_meta_dict)

    def __init__(self, value, **attributes):
        self._meta = None

        attributes = Attributes(attributes)
        super().__init__(value=value, attributes=attributes)

    @property
    def meta(self):
        return self._meta


class PlaceHolder(Feed):
    def __init__(self, **attributes):
        value = AnyValue

        attributes = {feed_type_field_name: feed_type_value_placeholder, **attributes}
        super().__init__(value=value, **attributes)

    def set_value(self, value):
        self.validate(value=value)
        self.set_value(value=value)


class Param(Feed):
    expected_types_container = (list, tuple)
    param_value_type_var_name = 'value_type'

    def __init__(self, value, **attributes):
        attributes = {feed_type_field_name: feed_type_value_param, **attributes}
        super().__init__(value=value, **attributes)

        if Param.param_value_type_var_name in self:
            expected_types = self.attributes[Param.param_value_type_var_name]
            if isinstance(expected_types, Param.expected_types_container):
                pass
            else:
                expected_types = [expected_types]
            validator = BasicTypeValidator(expected_types=expected_types)
            self.add_validators(validator)
            self.self_validate()


class Config(Param):
    def __init__(self, value, **attributes):
        attributes = {_DATA_TYPE_FIELD_NAME: _DATA_TYPE_VALUE_CONFIG, **attributes}
        super().__init__(value=value, **attributes)

