
from dag_pipe.helpers.elemental.attributes import AttributeBase, NotNullFieldMixin
from dag_pipe.helpers.collections.containers import MappingDict

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

