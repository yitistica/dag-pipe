
from dag_pipe.helpers.elemental.validator import Validator, FailedValidationError


def check_type(value, value_type):
    if value_type == 'str':
        if not isinstance(value, str):
            raise FailedValidationError()


