"""
to some extent:

for each class:
    we might have multiple methods that computes different things;

    but each callable means a method rather than the whole class;

"""
from dag_pipe.core.helpers.kernel_meta import check_kernel_meta, serialize_kernel_meta
from dag_pipe.core.utils.sys import hash_string

_HASH_PRECISION = 7


def _hash_kernel_meta(meta):
    meta_str = serialize_kernel_meta(meta)
    hash_ = hash_string(string=meta_str, precision=_HASH_PRECISION)
    return hash_


class KernelCollection(object):
    kernels = dict()


class Kernel(object):

    def __new__(cls, callable_, *args, **kwargs):
        kernel_meta = check_kernel_meta(callable_)
        id_ = _hash_kernel_meta(meta=kernel_meta)

        kernel = KernelCollection.kernels.get(id_)
        if not kernel:
            kernel = super().__new__(cls)
            kernel._id = id_
            kernel.kernel_meta = kernel_meta
            kernel._type = kernel_meta['kernel_type']
            kernel._callable = callable_
            KernelCollection.kernels[id_] = kernel
            return kernel
        else:
            return kernel

    def __init__(self, *args, **kwargs):
        pass

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type

    def run(self, *args, **kwargs):
        self._callable()


def function_a(a):
    return a + 1


def function_b(b):
    return b + 2


class Gaussian(object):

    def __init__(self):
        pass


