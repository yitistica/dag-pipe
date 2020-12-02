"""
to some extent:

for each class:
    we might have multiple methods that computes different things;

    but each callable means a method rather than the whole class;

"""
from dag_pipe.core.helpers.kernel_meta import build_function_meta, build_method_meta, serialize_kernel_meta
from dag_pipe.core.utils.types import hash_string, check_is_function, check_is_class

_HASH_PRECISION = 7


def _validate_callable(callable_):
    if check_is_function(callable_):
        return 'function'
    elif check_is_class(callable_):
        return 'class'
    else:
        raise TypeError('Not a callable.')  # TODO


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


class Kernel(object):
    def __new__(cls, callable_, *args, **kwargs):
        type_ = _validate_callable(callable_)

        if type_ == 'function':
            kernel_meta = build_function_meta(callable_)
        elif type_ == 'class':
            method_name = kwargs.get('method')
            if not method_name:
                raise TypeError(f"__init__() missing 1 required keyword argument: 'method'. ")
            kernel_meta = build_method_meta(callable_, method_name=method_name)
        else:
            raise TypeError(f" type_ ({type_}) is not supported.")

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


class MethodKernel(Kernel):

    def __new__(cls, callable_, *args, **kwargs):
        _method = kwargs.get('method')
        if not _method:
            raise TypeError(f"__init__() missing 1 required keyword argument: 'method'. ")

        kernel = super().__new__(*args, **kwargs)
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
