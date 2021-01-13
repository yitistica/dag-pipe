
from dag_pipe.helpers.elemental.validator import Validator, validator_factory
from dag_pipe.compartment.utils import check_data_type


class FailedValidationError(Exception):  # TEMP
    def __init__(self):
        message = f'failed validation.'
        super().__init__(message)


class UnmatchedDataTypeError(Exception):
    def __init__(self, expected_type, given_type):
        message = f'Given type <{given_type}> does not match the expected type <{expected_type}>.'
        super().__init__(message)


class BasicTypeValidator(Validator):
    def validator(self, value, expected_types):
        type_ = check_data_type(value)
        if type_ and (type_ not in expected_types):
            raise UnmatchedDataTypeError(expected_type=expected_types, given_type=type_)
