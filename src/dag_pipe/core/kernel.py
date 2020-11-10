"""
to some extent:

for each class:
    we might have multiple methods that computes different things;

    but each callable means a method rather than the whole class;

"""
from dag_pipe.core.helpers.kernel_meta import check_meta_meta, serialize_kernel_meta
from dag_pipe.core.utils.types import hash_string

_HASH_PRECISION = 7


def _hash_kernel_meta(meta):
    meta_str = serialize_kernel_meta(meta)
    hash_ = hash_string(string=meta_str, precision=_HASH_PRECISION)
    return hash_


class KernelCollection(object):
    kernels = dict()


class Kernel(object):

    def __new__(cls, function, *args, **kwargs):
        kernel_meta = check_meta_meta(function)
        id_ = _hash_kernel_meta(meta=kernel_meta)

        kernel = KernelCollection.kernels.get(id_)
        if not kernel:
            kernel = super().__new__(cls)
            kernel._id = id_
            kernel.kernel_meta = kernel_meta
            kernel._type = kernel_meta['kernel_type']
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

    @property
    def type(self):
        return self._type

    def run(self, *args, **kwargs):
        self._callable()


class FunctionPackager(object):
    def __init__(self, package_):
        pass

    def repackage_function(self, function):
        pass

    def init_state(self):
        pass


def function_a(a):
    return a + 1


def function_b(b):
    return b + 2


def add_class(cls):
    if 'a' in KernelCollection.kernels:
        KernelCollection.kernels['b'] = cls  # wrap the class
    else:
        KernelCollection.kernels['a'] = cls
    return cls


@add_class
class Gaussian(object):

    def __init__(self, a, b=2):
        self.a = a
        self.b = b



print(KernelCollection.kernels)