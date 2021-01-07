"""
palceholder:

attribute:

Examiner Mixin;

enforce attribute:

default value;

how to set default attribute: automate function, generated;
"""
from collections.abc import MutableMapping



class Element(object):
    def __new__(cls, value, **kwargs):
        if kwargs:
            pass
        self = super().__new__(cls)
        return self

    def __init__(self, *arg):
        self._value = value

    @property
    def value(self):
        return self._value


class Empty(object):
    pass