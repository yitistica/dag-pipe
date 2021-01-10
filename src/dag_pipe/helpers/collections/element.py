"""
default value;

validator

how to set default attribute: automate function, generated;

element constructor:

attribute

validator: not null, table_size, type


validator

serialize
"""
from dag_pipe.helpers.collections.attributes import Attributes
from dag_pipe.helpers.collections.validator import ValidatorSet

_PLACEHOLDER_VAR_NAME = 'place_holder'


class EmptyValue(object):
    pass


class ElementBase(object):
    def __init__(self, value, attributes):
        self._value = value
        self._attributes = attributes

    @property
    def value(self):
        return self._value

    def set_value(self, value):
        self._value = value

    @value.setter
    def value(self, value):
        self.set_value(value=value)

    @value.deleter
    def value(self):
        self._value = EmptyValue

    def if_empty_value(self):
        if self.value is EmptyValue:
            return True
        else:
            return False

    @property
    def attributes(self):
        return self._attributes

    def get_attri(self, field):
        return self.attributes[field]

    def __getitem__(self, field):
        return self.get_attri(field)

    def set_attri(self, field, value):
        self.attributes[field] = value

    def __setitem__(self, field, value):
        self.set_attri(field=field, value=value)


class Element(ElementBase):
    def __init__(self, value, attributes, validators=None):
        self.validator_set = ValidatorSet(*validators)
        self.validator_set.validate(value)
        super().__init__(value=value, attributes=attributes)

    def add_validator(self, validator):
        self.validator_set.add_validator(validator=validator)

    def validate(self, value):
        self.validator_set.validate(value)



class PlaceHolder(Element):
    def __init__(self, attribute_dict=None):
        value = EmptyValue

        if attribute_dict is None:
            attribute_dict = dict()

        attribute_dict = {_PLACEHOLDER_VAR_NAME: True, **attribute_dict}
        attributes = Attributes(attributes=attribute_dict, immutable_fields=[])
        super().__init__(value=value, attributes=attributes, validators=)

    def set_value(self, value):
        attributes = self.attributes
        del attributes[_PLACEHOLDER_VAR_NAME]
        super().__init__(value=value, attributes=attributes, validators=self.validator_set.validators)


class SetValidator(Validator):
    pass


class GetValidator(Validator):
    pass


class TypeValidator(Validator):
    pass


class Element(ElementBase):
    def __init__(self, *args, **kwargs):
        super(Element, self).__init__(value=args[0], attributes=kwargs)


place_holder = PlaceHolder({'a': 2})
print(type(place_holder))

print(place_holder.attributes[_PLACEHOLDER_VAR_NAME])

place_holder.value = 2
print(type(place_holder))


