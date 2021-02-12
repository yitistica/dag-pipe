"""
one process:
multiple arguments set
one process kernel;
one runtime manager;
one log;

preprocess is a type of process;

generate value;

results:
    both export results to db
    as an input of

result template converter:

default:

if empty:

when get then delete


result could be batch, and different params, and size;

dont use pickle to serialize id, because different machine and float can reduce the liability;

"""
from dag_pipe.helpers.elemental.element import Element
from dag_pipe.helpers.collections.containers import MappingDict
from dag_pipe.compartment.attributes import ResultMetaAttributes, ResultAttributes
from dag_pipe.helpers.elemental.attributes import AttributeBase, NotNullFieldMixin


class Result(Element):
    meta_dict = {'type': 'result'}

    def __init__(self, value, **attributes):
        self._meta = ResultMetaAttributes(self.meta_dict)

        attributes = ResultAttributes(attributes)
        super().__init__(value=value, attributes=attributes)

    @property
    def meta(self):
        return self._meta

    def validators_setting(self):
        return self.validator_set.summary


class KernelResults(object):

    def __init__(self):
        pass

    def admit_result(self, value, **attributes):
        pass


class KernelResultsCollector(object):
    def __init__(self):
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

