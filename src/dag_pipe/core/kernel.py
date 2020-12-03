"""
to some extent:

for each class:
    we might have multiple methods that computes different things;

    but each callable means a method rather than the whole class;

"""
from dag_pipe.core.helpers.kernel_meta import build_function_meta, build_method_meta, serialize_kernel_meta
from dag_pipe.core.utils.types import hash_string, check_is_function, check_is_class

_HASH_PRECISION = 7


def _hash_kernel_meta(meta):
    meta_str = serialize_kernel_meta(meta)
    hash_ = hash_string(string=meta_str, precision=_HASH_PRECISION)
    return hash_


class MethodNotFoundError(Exception):
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        if self.message:
            return f'MethodNotFoundError, {self.message}'
        else:
            return 'MethodNotFoundError has been raised'


class KernelCollection(object):  # TEMP
    kernels = dict()


class CallableMeta(object):
    def __init__(self):
        pass


class Kernel(object):
    def __new__(cls, callable_, kernel_meta, *args, **kwargs):
        id_ = _hash_kernel_meta(meta=kernel_meta)
        kernel = KernelCollection.kernels.get(id_)

        if not kernel:
            kernel = super().__new__(cls)
            kernel._id = id_
            kernel.kernel_meta = kernel_meta
            kernel._callable = callable_
            KernelCollection.kernels[kernel._id] = kernel
        else:
            pass

        return kernel

    def __init__(self, *args, **kwargs):
        pass

    @property
    def id(self):
        return self._id

    @property
    def callable(self):
        return self.kernel._callable


class FunctionKernel(Kernel):
    def __new__(cls, callable_, *args, **kwargs):

        if not check_is_function(object_=callable_):
            raise TypeError(f"callable_ ({callable_}) by type ({type(callable_)}) is not a function.")
        kernel_meta = build_function_meta(callable_)
        kernel = super().__new__(callable_=callable_, kernel_meta=kernel_meta, *args, **kwargs)

        return kernel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BoundKernel(Kernel):
    def __new__(cls, method_class, method_name, *args, **kwargs):
        if not check_is_class(method_class):
            raise TypeError(f"method_class ({method_class}) by type ({type(method_class)}) is not a class.")

        if not method_name:
            raise TypeError(f"__init__() missing 1 required keyword argument: 'method'. ")

        kernel_meta = build_method_meta(class_=method_class, method_name=)
        kernel = super().__new__(callable_=callable_, *args, **kwargs)
        return kernel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _verify_method(self, method_name):
        method = getattr(self.callable, method_name)
        print(method)

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



def func(a):
    return None


func()
