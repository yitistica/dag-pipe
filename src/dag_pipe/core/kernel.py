"""
to some extent:

for each class:
    we might have multiple methods that computes different things;

    but each callable means a method rather than the whole class;

"""
from dag_pipe.core.helpers.kernel_meta import get_meta, serialize_kernel_meta
from dag_pipe.core.utils.types import hash_string, check_is_function

_HASH_PRECISION = 7


def _validate_function(function):
    if check_is_function(function):
        return function
    else:
        raise TypeError('Not a function.')  # TODO


def _hash_kernel_meta(meta):
    meta_str = serialize_kernel_meta(meta)
    hash_ = hash_string(string=meta_str, precision=_HASH_PRECISION)
    return hash_


class KernelCollection(object):  # TEMP
    kernels = dict()


class Kernel(object):
    def __new__(cls, function, *args, **kwargs):
        function = _validate_function(function)
        kernel_meta = get_meta(function)
        id_ = _hash_kernel_meta(meta=kernel_meta)

        kernel = KernelCollection.kernels.get(id_)
        if not kernel:
            kernel = super().__new__(cls)
            kernel._id = id_
            kernel.kernel_meta = kernel_meta
            kernel._callable = function
            KernelCollection.kernels[id_] = kernel
            return kernel
        else:
            return kernel

    def __init__(self, *args, **kwargs):
        pass

    @property
    def id(self):
        return self._id

    def exec_kernel(self, *args, **kwargs):
        return self._callable(*args, **kwargs)

