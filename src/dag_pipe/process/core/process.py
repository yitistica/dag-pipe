"""
one process:
multiple arguments set
one process kernel;
one runtime manager;
one log;

preprocess is a type of process;

generate value;

"""
from dag_pipe.helpers.elemental.attributes import AttributeBase, NotNullFieldMixin


class ProcessComponent(object):
    pass


class ProcessAttributes(AttributeBase, NotNullFieldMixin):
    def __init__(self, attributes=(), not_null_fields=None, null_forms=None):

        if not not_null_fields:
            not_null_fields = []

        if null_forms is None:
            null_forms = [None]

        AttributeBase.__init__(self, attributes=attributes)
        NotNullFieldMixin.__init__(self, fields=not_null_fields)
        for field in not_null_fields:
            self._check_null(field=field, null_forms=null_forms)


