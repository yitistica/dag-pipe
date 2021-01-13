from dag_pipe.helpers.elemental.element import Element
from dag_pipe.helpers.elemental.attributes import Attributes
from dag_pipe.compartment.validators import BasicTypeValidator


_FEED_TYPE_PLACEHOLDER = 'placeholder'
_FEED_TYPE_PARAM = 'param'

# data types:
_DATA_TYPE_FIELD_NAME = 'data_type'
_DATA_TYPE_VALUE_CONFIG = 'config'


class AnyValue(object):
    pass


class EmptyValue(object):
    pass


class Feed(Element):
    meta_dict = {'type': 'feed'}

    def __init__(self, value, **attributes):
        self._meta = Attributes(self.meta_dict)

        attributes = Attributes(attributes)
        super().__init__(value=value, attributes=attributes)

    @property
    def meta(self):
        return self._meta


class PlaceHolder(Feed):
    meta_dict = {'type': _FEED_TYPE_PLACEHOLDER}

    def __init__(self, **attributes):
        value = AnyValue
        super().__init__(value=value, **attributes)

    def set_value(self, value):
        self.validate(value=value)
        self.set_value(value=value)


class Param(Feed):
    meta_dict = {'type': _FEED_TYPE_PARAM}
    _expected_types_container = (list, tuple)
    _param_value_type_var_name = 'value_type'

    def __init__(self, value, **attributes):
        super().__init__(value=value, **attributes)

        if self._param_value_type_var_name in self.attributes:
            expected_types = self.attributes[Param._param_value_type_var_name]
            if isinstance(expected_types, self._expected_types_container):
                pass
            else:
                expected_types = [expected_types]
            validator = BasicTypeValidator(expected_types=expected_types)
            self.add_validators(validator)
            self.self_validate()


class Config(Param):
    meta_dict = {'type': _DATA_TYPE_VALUE_CONFIG}

    def __init__(self, value, **attributes):
        super().__init__(value=value, **attributes)

