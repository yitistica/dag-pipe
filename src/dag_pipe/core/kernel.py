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


class MethodNotImplementError(Exception):
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
        return self._callable

    def call(self, *args, **kwargs):
        return self.callable(*args, **kwargs)


class FunctionKernel(Kernel):
    def __new__(cls, callable_, *args, **kwargs):

        if not check_is_function(object_=callable_):
            raise TypeError(f"callable_ ({callable_}) by type ({type(callable_)}) is not a function.")
        kernel_meta = build_function_meta(callable_)
        kernel = super().__new__(cls, callable_=callable_, kernel_meta=kernel_meta, *args, **kwargs)

        return kernel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ClassKernel(Kernel):
    def __new__(cls, class_, method_name, *args, **kwargs):
        if not check_is_class(class_):
            raise TypeError(f"method_class ({class_}) by type ({type(class_)}) is not a class.")

        if not method_name:
            raise TypeError(f"__init__() missing 1 required keyword argument: 'method'. ")

        callable_ = ClassKernel._verify_method(class_=class_, method_name=method_name)
        kernel_meta = build_method_meta(class_=class_, method_name=method_name)
        kernel = super().__new__(cls, callable_=callable_, kernel_meta=kernel_meta, *args, **kwargs)
        kernel._class = class_
        return kernel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def _verify_method(class_, method_name):
        try:
            method = getattr(class_, method_name)
        except AttributeError:
            raise MethodNotImplementError(f'method ({method_name}) is not implement in the ({class_}) class.')

        return method


class InitKernel(ClassKernel):
    def __new__(cls, class_, *args, **kwargs):
        kernel = super().__new__(cls, class_=class_, method_name='__init__', *args, **kwargs)
        return kernel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def init(self, *args, **kwargs):
        instance = self._class(*args, **kwargs)
        return instance

    def call(self, *args, **kwargs):
        return self.init(*args, **kwargs)


class MethodKernel(ClassKernel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _verify_instance_argument(self, *args, **kwargs):
        instance = args[0]
        if not isinstance(instance, self._class):
            raise TypeError(f'instance ({instance}) is not an instance of the class of the kernel ({self._class}).')

        args = tuple(arg for index, arg in enumerate(args) if index > 0)

        return instance, args, kwargs

    def call(self, *args, **kwargs):
        instance, args, kwargs = self._verify_instance_argument(*args, **kwargs)
        return self.callable(instance, *args, **kwargs)


class ClassMethodKernel(ClassKernel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _verify_class_argument(self, *args, **kwargs):
        cls = args[0]
        if cls is not self._class:
            raise TypeError(f'instance ({cls}) is not the class of the kernel ({self._class}).')

        args = tuple(arg for index, arg in enumerate(args) if index > 0)

        return cls, args, kwargs

    def call(self, *args, **kwargs):
        cls, args, kwargs = self._verify_class_argument(*args, **kwargs)
        return self.callable(cls, *args, **kwargs)


class StaticMethodKernel(ClassKernel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def call(self, *args, **kwargs):
        return self.callable(*args, **kwargs)

