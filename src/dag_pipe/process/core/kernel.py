
from dag_pipe.helpers.elemental.attributes import AttributeBase, NotNullFieldMixin
from dag_pipe.helpers.kernel_meta import build_function_meta, build_method_meta, serialize_kernel_meta
from dag_pipe.helpers.collections.containers import MappingDict
from dag_pipe.utils.types import check_is_function, check_is_class
from dag_pipe.utils.identifier import hash_string


_HASH_PRECISION = 7

_KERNEL_NULL_FORM = [None, ]


class OccupiedKernelIDError(Exception):
    def __init__(self, kernel_id):
        message = f'Kernel by the id <{kernel_id}> is taken, cannot be reset.'
        super().__init__(message)


class KernelAttributes(AttributeBase, NotNullFieldMixin):
    def __init__(self, kernel_attributes=(), not_null_fields=None, null_forms=None):

        if not not_null_fields:
            not_null_fields = []

        if null_forms is None:
            null_forms = [None]

        AttributeBase.__init__(self, attributes=kernel_attributes)
        NotNullFieldMixin.__init__(self, fields=not_null_fields)
        for field in not_null_fields:
            self._check_null(field=field, null_forms=null_forms)


class _KernelStorage(MappingDict):
    def __init__(self, **kernel_dict):
        super().__init__()

        for kernel_id, kernel in kernel_dict.items():
            self[kernel_id] = kernel

    def _set(self, kernel_id, kernel):
        super()._set(key=kernel_id, value=kernel)

    def __contains__(self, kernel_id):
        return super().__contains__(key=kernel_id)


class KernelNamespace(object):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self):
        self._kernels = _KernelStorage()

    @property
    def kernels(self):
        return self._kernels

    def admit_kernel(self, kernel_id, kernel):
        if kernel_id not in self:
            self._kernels[kernel_id] = kernel
        else:
            raise OccupiedKernelIDError(kernel_id=kernel_id)

    def get_kernel(self, kernel_id):
        return self._kernels[kernel_id]

    def __contains__(self, kernel_id):
        return kernel_id in self._kernels


class Kernel(object):
    # _identifier_field = 'identifier'
    _location_field = 'location'
    _meta_not_null_fields = [_location_field]

    def __new__(cls, callable_, attributes, *args, **kwargs):

        _attributes = KernelAttributes(kernel_attributes=attributes,
                                       not_null_fields=cls._meta_not_null_fields,
                                       null_forms=_KERNEL_NULL_FORM)

        kernel = super().__new__(cls)
        kernel._attributes = _attributes
        kernel._callable = callable_

        return kernel

    def __init__(self, *args, **kwargs):
        pass

    @property
    def attributes(self):
        return self._attributes

    @property
    def callable(self):
        return self._callable

    def call(self, *args, **kwargs):
        return self.callable(*args, **kwargs)


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
