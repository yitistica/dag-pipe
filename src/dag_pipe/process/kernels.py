"""
to some extent:

"""
from dag_pipe.helpers.kernel_meta import build_function_meta, build_method_meta, serialize_kernel_meta
from dag_pipe.utils.types import hash_string, check_is_function, check_is_class
from dag_pipe.process.core.kernel import Kernel
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


class FunctionKernel(Kernel):
    def __new__(cls, callable_, *args, **kwargs):

        if not check_is_function(object_=callable_):
            raise TypeError(f"callable_ ({callable_}) by type ({type(callable_)}) is not a function.")

        kernel_meta = build_function_meta(callable_)
        attributes = kwargs.pop('attributes', None)
        if not attributes:
            attributes = dict()
        attributes = {**attributes, **kernel_meta}

        kernel = super().__new__(cls, callable_=callable_, attributes=attributes, *args, **kwargs)

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
        attributes = kwargs.pop('attributes', None)
        if not attributes:
            attributes = dict()
        attributes = {**attributes, **kernel_meta}

        kernel = super().__new__(cls, callable_=callable_, attributes=attributes, *args, **kwargs)
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

        attributes = kwargs.pop('attributes', None)
        if not attributes:
            attributes = dict()

        kernel = super().__new__(cls, class_=class_, method_name='__init__', attributes=attributes, *args, **kwargs)
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



from inspect import signature
from typing import Union, Optional
import pandas as pd


def func(a: str, b: Optional[Union[str, int, pd.DataFrame]] = None, *args, **kwargs):
    return a


class AClass(object):

    def __init__(self, *args, **kwargs):
        pass

    def method_a(self, c: list, b: Optional[Union[str, int, pd.DataFrame]] = None,):
        return b

    @classmethod
    def method_b(cls, b: Optional[Union[str, int]] = None, ):
        return b


function_kernel = MethodKernel(AClass, 'method_a')

sig = signature(function_kernel.callable)
anotation = sig.parameters['self'].kind

print(anotation)