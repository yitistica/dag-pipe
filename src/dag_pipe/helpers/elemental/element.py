
from dag_pipe.helpers.elemental.attributes import Attributes
from dag_pipe.helpers.elemental.validator import Validator, ValidatorSet


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

    def add_attributes(self, attributes, override=True):
        if isinstance(attributes, Attributes):
            for field, value in attributes.items():
                if override:
                    self.set_attri(field=field, value=value)
                else:
                    if field not in self.attributes:
                        self.set_attri(field=field, value=value)
        else:
            raise TypeError(f"<{attributes}> is not an instance of Attributes")

    @attributes.deleter
    def attributes(self):
        for field in self.attributes:
            del self.attributes[field]

    def get_attri(self, field):
        return self.attributes[field]

    def __getitem__(self, field):
        return self.get_attri(field)

    def set_attri(self, field, value):
        self.attributes[field] = value

    def __setitem__(self, field, value):
        self.set_attri(field=field, value=value)

    def __contains__(self, field):
        return field in self.attributes

    def __add__(self, attributes):
        self.add_attributes(attributes=attributes)


class Element(ElementBase):
    def __init__(self, value, attributes=None, validators=None):
        if not validators:
            validators = ()
        self.validator_set = ValidatorSet()
        self.add_validators(*validators)

        if not attributes:
            attributes = Attributes()

        super().__init__(value=value, attributes=attributes)

    def add_validators(self, *validators):
        self.validator_set.add_validators(*validators)

    def validate(self, value):
        self.validator_set.validate(value=value)

    def self_validate(self):
        self.validator_set.validate(value=self.value)

    def _add_component(self, component):
        if isinstance(component, Attributes):
            self.add_attributes(attributes=component)
        elif isinstance(component, (Validator, ValidatorSet)):
            self.add_validators(component)
        else:
            TypeError(f"object {component} is not an instance of Attributes, Validator or ValidatorSet.")

    def __add__(self, component):
        self._add_component(component=component)
