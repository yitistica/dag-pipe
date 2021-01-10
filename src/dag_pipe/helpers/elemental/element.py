
from dag_pipe.helpers.elemental.attributes import Attributes
from dag_pipe.helpers.elemental.validator import ValidatorSet


class EmptyValue(object):
    pass


class ElementBase(object):
    def __init__(self, value, attributes):
        self._value = value

        if isinstance(attributes, Attributes):
            self._attributes = attributes
        else:
            raise TypeError(f"attributes <{attributes}> is not an instance of Attributes.")

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
    def __init__(self, value, attributes=None, validators=None):
        if not validators:
            validators = ()
        self.validator_set = ValidatorSet(*validators)

        if not attributes:
            attributes = Attributes()

        super().__init__(value=value, attributes=attributes)

    def add_validator(self, validator):
        self.validator_set.add_validator(validator=validator)

    def validate(self, value):
        self.validator_set.validate(value=value)
