from inspect import signature
from typing import Union, Optional


def func(a: str, b: Optional[Union[str, int]] = None, *args, **kwargs):
    return a

class AClass(object):

    def __init__(self, *args, **kwargs):
        pass

    def method_a(self, b: Optional[Union[str, int]] = None, ):
        return b

    @classmethod
    def method_a(cls, b: Optional[Union[str, int]] = None, ):
        return b


sig = signature(AClass.method_a)

print(sig.parameters)
