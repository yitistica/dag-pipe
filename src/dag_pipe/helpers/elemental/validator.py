
from abc import abstractmethod, ABCMeta


def validator_factory(validator_name, callable_, **defaults):

    def validator_method(self, value, **kwargs):
        validation = callable_(value, **kwargs)
        return validation

    preset_params = defaults

    attributedict = {'preset_params': preset_params,  # change this if class attribute preset_params is renamed
                     Validator.validator.__name__: validator_method
                     }

    validator_class = type(validator_name, (Validator, ), attributedict)

    return validator_class


class Validator(object, metaclass=ABCMeta):
    preset_params = dict()
    expose_params = []

    def __init__(self, **params):
        params = {**self.__class__.preset_params, **params}
        self._params = params

    @property
    def params(self):
        return self._params

    @property
    def summary(self):
        validator_sumary = {'name': self.__class__.__name__,
                            'params': self.params}
        return validator_sumary

    @abstractmethod
    def validator(self, value, **kwargs):
        raise NotImplementedError()

    def validate(self, value):
        self.validator(value=value, **self.params)

    def __call__(self, value):
        self.validate(value=value)


class _ValidatorResult(object):
    # TODO implement a validator result, for logging;
    pass


class ValidatorSet(object):
    def __init__(self, *validators):
        self.validators = []
        self.add_validators(*validators)

    def add_validators(self, *validators):
        for validator in validators:
            if isinstance(validator, Validator):
                self.validators.append(validator)
            elif isinstance(validator, ValidatorSet):
                for _validator in validator.validators:
                    self.validators.append(_validator)
            else:
                raise TypeError(f"object {validator} is not an instance of Validator or ValidatorSet.")

    def validate(self, value):
        for validator in self.validators:
            validator.validate(value)

    @property
    def summary(self):
        summary = []
        for validator in self.validators:
            summary.append(validator.summary)
        return summary
