
class PassValidation(object):
    pass


class FailedValidationError(Exception):  # TEMP
    def __init__(self):
        message = f'failed validation.'
        super().__init__(message)


class Validator(object):
    def __init__(self, validation_callable=None, **params):
        self.validation_callable = PassValidation
        if params:
            self.params = params
        else:
            self.params = dict()

        if validation_callable:
            self.add_validation(validation_callable=validation_callable)

    def add_validation(self, validation_callable):
        if not callable(validation_callable):
            raise TypeError(f'{validation_callable} is not a callable.')
        else:
            self.validation_callable = validation_callable

    def validate(self, value):
        if self.validation_callable is not PassValidation:
            self.validation_callable(value, **self.params)


class ValidatorSet(object):
    def __init__(self, *validators):
        self.validators = []
        self.add_validators(*validators)

    def add_validators(self, *validators):
        for validator in validators:
            if isinstance(validator, Validator):
                self.validators.append(validator)
            if isinstance(validator, ValidatorSet):
                for _validator in validator.validators:
                    self.validators.append(_validator)
            else:
                raise TypeError(f"object {validator} is not an instance of Validator or ValidatorSet.")

    def validate(self, value):
        for validator in self.validators:
            validator.validate(value)
