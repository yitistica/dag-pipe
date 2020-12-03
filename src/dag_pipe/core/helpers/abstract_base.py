"""

container:

"""

from collections import OrderedDict


class Meta(OrderedDict):
    def __init__(self, *args, **kwargs):
        super.__init__(*args, *kwargs)
