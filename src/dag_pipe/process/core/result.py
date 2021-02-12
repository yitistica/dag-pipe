"""
one process:
multiple arguments set
one process kernel;
one runtime manager;
one log;

preprocess is a type of process;

generate value;

if the result is not satisfy, rerun the process. basically an assessment;

results:
    both export results to db
    as an input of

result template converter:

default:

if empty:

when get then delete



"""
from dag_pipe.helpers.elemental.attributes import AttributeBase, NotNullFieldMixin


class ProcessResult(object):
    pass


class ProcessAttributes(AttributeBase, NotNullFieldMixin):
    def __init__(self, attributes=(), not_null_fields=None, null_forms=None):

        if not not_null_fields:
            not_null_fields = []

        if null_forms is None:
            null_forms = [None]

        AttributeBase.__init__(self, attributes=attributes)
        NotNullFieldMixin.__init__(self, fields=not_null_fields)
        for field in not_null_fields:
            self._check_null(field=field, null_forms=null_forms)


class OccupiedProcessIDError(Exception):
    def __init__(self, kernel_id):
        message = f'Kernel by the id <{kernel_id}> is taken, cannot be reset.'
        super().__init__(message)

