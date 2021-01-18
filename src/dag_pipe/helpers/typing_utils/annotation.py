"""

Notes:
    A:
class inspect.Parameter.kind
(source: https://docs.python.org/3/library/inspect.html)
1. POSITIONAL_ONLY: Value must be supplied as a positional argument. Positional only parameters are those which appear
before a / entry (if present) in a Python function definition.
2. POSITIONAL_OR_KEYWORD: Value may be supplied as either a keyword or positional argument.
3. KEYWORD_ONLY: Value must be supplied as a keyword argument. Keyword only parameters are those which appear
after a * or *args entry in a Python function definition.
4. VAR_POSITIONAL: A tuple of positional arguments that aren’t bound to any other parameter. This corresponds to a
*args parameter in a Python function definition.
5. VAR_KEYWORD: A dict of keyword arguments that aren’t bound to any other parameter. This corresponds to a **kwargs
parameter in a Python function definition.
And,
1) / indicates that some function parameters must be specified positionally and cannot be used as keyword arguments;
2) The * indicates the end of the positional arguments;
e.g., func(param1, param2, /, param3, *, param4, param5):
- param1 and param2: positional only;
- param3: positional or keyword;
- param4 and param5: keyword only.

output annotation;
"""

from collections import OrderedDict
from inspect import signature
from typing import Union, Optional


def get_annotation_from_callable(callable_):
    signature_ = signature(callable_)



def check_type(given, expected):
    pass



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


sig = signature(AClass.__init__)

print(sig.parameters['self'].kind)
