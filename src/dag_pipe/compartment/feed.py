"""
Feed: the basic element of argument, results;
"""

from dag_pipe.helpers.elemental.element import Element
from dag_pipe.compartment.attributes import FeedMetaAttributes, FeedAttributes, FEED_ID_VAR_NAME
from dag_pipe.compartment.validators import BasicTypeValidator, DataFrameValidator


_FEED_TYPE_PLACEHOLDER = 'placeholder'
_FEED_TYPE_PLACEHOLDER_DATAFRAME = 'dataframe_holder'
_FEED_TYPE_PARAM = 'param'
_FEED_TYPE_CONFIG = 'config'

_VALIDATOR_PARAMS_ATTRIBUTE_FIELD_NAME = '_validator_params'


class AnyValue(object):
    pass


class EmptyValue(object):
    pass


class Feed(Element):
    meta_dict = {'type': 'feed'}

    def __init__(self, value, **attributes):
        self._meta = FeedMetaAttributes(self.meta_dict)

        attributes = FeedAttributes(attributes)
        super().__init__(value=value, attributes=attributes)

    @property
    def meta(self):
        return self._meta

    def validators_setting(self):
        return self.validator_set.summary


class PlaceHolder(Feed):
    meta_dict = {'type': _FEED_TYPE_PLACEHOLDER}

    def __init__(self, **attributes):
        value = AnyValue
        super().__init__(value=value, **attributes)

    def set_value(self, value):
        self.validate(value=value)
        super().set_value(value=value)


class Param(Feed):
    meta_dict = {'type': _FEED_TYPE_PARAM}
    _expected_types_container = (list, tuple, set)
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
    meta_dict = {'type': _FEED_TYPE_CONFIG}

    def __init__(self, value, **attributes):
        super().__init__(value=value, **attributes)


class DataFrameHolder(PlaceHolder):
    meta_dict = {'type': _FEED_TYPE_PLACEHOLDER_DATAFRAME}

    def __init__(self, **attributes):

        validator_params = dict()
        _attributes = dict()
        # regroup attributes that belong to validators;
        for attri_field, attri_value in attributes.items():
            if attri_field in DataFrameValidator.expose_params:
                validator_params[attri_field] = attri_value
            else:
                _attributes[attri_field] = attri_value

        _attributes = {**_attributes, _VALIDATOR_PARAMS_ATTRIBUTE_FIELD_NAME: validator_params}

        super().__init__(**_attributes)
        validator = DataFrameValidator(**validator_params)
        self.add_validators(validator)
