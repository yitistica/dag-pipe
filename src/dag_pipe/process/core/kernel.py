"""

location hash;
"""
from dag_pipe.helpers.elemental.attributes import AttributeBase, NotNullFieldMixin
from dag_pipe.helpers.collections.containers import MappingDict

_KERNEL_NULL_FORM = [None, ]


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


class KernelNamespace(object):
    kernels = dict()

    def __new__(cls, namespace, *args, **kwargs):
        pass

    def __init__(self, namespace):
        pass

    def add_kernel(self, ):
        pass

    def get_kernel(self, id_):
        pass


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