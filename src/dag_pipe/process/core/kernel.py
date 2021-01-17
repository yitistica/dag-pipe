"""

location hash;
"""
from dag_pipe.helpers.elemental.attributes import AttributeBase, NotNullFieldMixin
from dag_pipe.helpers.collections.containers import MappingDict

_KERNEL_NULL_FORM = [None, ]


class OccupiedKernelIDError(Exception):
    def __init__(self, kernel_id):
        message = f'Kernel by the id <{kernel_id}> is taken, cannot be reset.'
        super().__init__(message)


class KernelAttributes(AttributeBase, NotNullFieldMixin):
    def __init__(self, meta=(), not_null_fields=None, null_forms=None):

        if not not_null_fields:
            not_null_fields = []

        if null_forms is None:
            null_forms = [None]

        AttributeBase.__init__(self, attributes=meta)
        NotNullFieldMixin.__init__(self, fields=not_null_fields)
        for field in not_null_fields:
            self._check_null(field=field, null_forms=null_forms)


class KernelStorage(MappingDict):
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
        self.kernels = KernelStorage()

    def add_kernel(self, kernel):
        kernel_id = kernel.id
        if kernel_id not in self:
            self.kernels[kernel_id] = kernel
        else:
            raise OccupiedKernelIDError(kernel_id=kernel_id)

    def get_kernel(self, kernel_id):
        return self.kernels[kernel_id]

    def __contains__(self, kernel):
        if isinstance(kernel, Kernel):
            return kernel.id in self.kernels
        else:
            return kernel in self.kernels


class Kernel(object):
    _identifier_field = 'identifier'
    _meta_not_null_fields = [_identifier_field]

    def __new__(cls, namespace, callable_, attributes, *args, **kwargs):

        _attributes = KernelAttributes(meta=attributes,
                                       not_null_fields=cls._meta_not_null_fields,
                                       null_forms=_KERNEL_NULL_FORM)

        identifier = _attributes[cls._identifier_field]
        kernel = namespace.get_kernel(identifier)

        if not kernel:
            kernel = super().__new__(cls)
            kernel._attributes = _attributes
            kernel._callable = callable_
            namespace.add_kernel(kernel)
        else:
            pass

        return kernel

    def __init__(self, namespace, callable_, attributes, *args, **kwargs):
        pass

    @property
    def attributes(self):
        return self._attributes

    @property
    def id(self):
        return self.attributes[self._identifier_field]

    @property
    def callable(self):
        return self._callable

    def call(self, *args, **kwargs):
        return self.callable(*args, **kwargs)