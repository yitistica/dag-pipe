"""
to some extent:

for each class:
    we might have multiple methods that computes different things;

    but each callable means a method rather than the whole class;

"""
from dag_pipe.core.helpers.kernel_meta import get_meta, serialize_kernel_meta
from dag_pipe.core.utils.types import hash_string, check_is_function, check_is_class

_HASH_PRECISION = 7


def _validate_callable(callable_):
    if check_is_function(callable_):
        return callable_
    elif check_is_class(callable_):
        return callable_
    else:
        raise TypeError('Not a callable.')  # TODO


def _hash_kernel_meta(meta):
    meta_str = serialize_kernel_meta(meta)
    hash_ = hash_string(string=meta_str, precision=_HASH_PRECISION)
    return hash_


class KernelCollection(object):  # TEMP
    kernels = dict()


class Kernel(object):
    def __new__(cls, callable_, *args, **kwargs):
        callable_ = _validate_callable(callable_)
        kernel_meta = get_meta(callable_)
        id_ = _hash_kernel_meta(meta=kernel_meta)

        kernel = KernelCollection.kernels.get(id_)
        if not kernel:
            kernel = super().__new__(cls)
            kernel._id = id_
            kernel.kernel_meta = kernel_meta
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
    def callable(self):
        return self.kernel._callable


class MethodKernel(Kernel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def call(self):
        pass


class InitKernel(MethodKernel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def call(self):
        pass


class Gaussian(object):
    def __init__(self, a, b=2):
        self.a = a
        self.b = b

    def method_a(self, a):
        return a + self.a




