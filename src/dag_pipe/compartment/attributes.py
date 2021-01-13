from dag_pipe.helpers.elemental.attributes import Attributes


class MetaAttributes(Attributes):
    def __init__(self, attributes):
        super().__init__(attributes=attributes, immutable_fields=['name'])
