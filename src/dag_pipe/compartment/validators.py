import pandas as pd

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


class UnfoundDataFrameColumnsError(Exception):
    def __init__(self, given_column):
        message = f'column <{given_column}> is not in the given dataframe.'
        super().__init__(message)


class UnmatchedDataFrameSizeError(Exception):
    def __init__(self, row_or_col, expected_size, given_size, test_type):
        message = f"Test for (actual_size {test_type} expected_size) on the size of dataframe's <{row_or_col}>: " \
                  f"given size <{given_size}>, does not match the expected size <{expected_size}>."
        super().__init__(message)


class BasicTypeValidator(Validator):
    def validator(self, value, expected_types):
        type_ = check_data_type(value)
        if type_ and (type_ not in expected_types):
            raise UnmatchedDataTypeError(expected_type=expected_types, given_type=type_)


class DataFrameValidator(Validator):
    expose_params = ['columns', 'row_size', 'col_size', 'row_test', 'col_test']

    @staticmethod
    def _check_if_data_frame(value):
        if not isinstance(value, pd.DataFrame):
            raise UnmatchedDataTypeError(expected_type=pd.DataFrame, given_type=type(value))

    @staticmethod
    def _contain_columns(value, columns):
        for col in columns:
            if col not in value.columns:
                raise UnfoundDataFrameColumnsError(given_column=col)

    @staticmethod
    def _require_size(value, row_size=None, col_size=None, row_test=None, col_test=None):

        # default:
        if not row_test:
            row_test = '=='
        if not col_test:
            col_test = '=='

        actual_row_size, actual_col_size = value.shape

        raise_result = False
        for compare_tuple in [('row', actual_row_size, row_size, row_test),
                              ('column', actual_col_size, col_size, col_test)]:

            row_or_col, actual_size, expected_size, test = compare_tuple
            if expected_size:
                if test == '==':
                    if not (actual_size == expected_size):
                        raise_result = True
                elif test == '>=':
                    if not (actual_size >= expected_size):
                        raise_result = True
                elif test == '>':
                    if not (actual_size < expected_size):
                        raise_result = True
                elif test == '<':
                    if not (actual_size < expected_size):
                        raise_result = True
                elif test == '<=':
                    if not (actual_size <= expected_size):
                        raise_result = True
                else:
                    raise NotImplementedError(f'test <{test} is not implemented.')

                if raise_result:
                    raise UnmatchedDataFrameSizeError(row_or_col=row_or_col, expected_size=expected_size,
                                                      given_size=actual_size, test_type=test)

    def validator(self, value, **kwargs):
        DataFrameValidator._check_if_data_frame(value=value)

        columns = kwargs.get('columns')
        if columns:
            DataFrameValidator._contain_columns(value=value, columns=columns)

        row_size = kwargs.get('row_size')
        col_size = kwargs.get('col_size')

        row_test = kwargs.get('row_test')
        col_test = kwargs.get('col_test')

        if row_size or col_size:
            DataFrameValidator._require_size(value, row_size=row_size, col_size=col_size,
                                             row_test=row_test, col_test=col_test)
