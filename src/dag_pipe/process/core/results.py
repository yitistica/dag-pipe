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

same value id

.create(dimension, auto_increment).

result could be batch, and different params, and size; but should put param into a sorter;


result registery?
"""
from dag_pipe.compartment.feed import Feed
from dag_pipe.helpers.collections.containers import ValueCollection  # it probably shouldnt be
from dag_pipe.compartment.attributes import ResultMetaAttributes, ResultAttributes
from dag_pipe.helpers.elemental.attributes import AttributeBase, NotNullFieldMixin


class Result(Feed):
    meta_dict = {'type': 'result'}

    def __init__(self, value, **attributes):
        super().__init__(value=value, attributes=attributes)


class KernelResultPool(object):  # different arguments, but same partition;

    def __init__(self):
        self._results = []

    def admit_result(self, key, result):
        if not isinstance(result, Result):
            raise TypeError(f"result (type {type(Result)}) is not of the type Result.")
        else:
            self._results.append((key, result))

    def retrieve_result(self):
        if len(self._results) == 1:
            return self._results[0][1]
        else:
            results = [result[1] for result in self._results]
            results = ValueCollection(results)

        return results


class KernelResultsCollector(object):
    def __init__(self):
        self._alias = dict()
        self._pools = []

    @property
    def pool_size(self):
        return len(self._pools)

    def add_partition(self, alias=None):
        if alias and (not isinstance(alias, str)):
            raise TypeError(f"please use str type to name the partition.")
        elif alias:
            current_partition_no = len(self._pools)
            self._alias[alias] = current_partition_no

        self._pools.append(KernelResultPool())

    def get_result_pool(self, identifier):
        if isinstance(identifier, int):
            kernel_result_pool = self._pools[identifier]
        elif isinstance(identifier, str):
            kernel_result_pool = self._pools[self._alias[identifier]]
        else:
            raise TypeError(f"key type is not acceptable.")

        return kernel_result_pool

    def admit_result(self, identifier, key, result):
        kernel_result_pool = self.get_result_pool(identifier=identifier)
        kernel_result_pool.admit_result(key=key, result=result)

    def retrieve_result(self, identifier):
        result_pool = self.get_result_pool(identifier=identifier)
        return result_pool.retrieve_result()


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

