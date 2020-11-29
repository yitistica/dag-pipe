"""
Params:
- process set at each level:
- global params:
- runtime params:
- logging params: ?

conditional params: if certain argument is valid;
pickle param


runtime params:

be able to pass in different argument prefix:

@process.func(analyzer=(func1, func2))

pass keyword argument:


"""
from collections import OrderedDict
import inspect


class EmptyArgument(object):
    pass


def _inspect_function_params(function):
    signature = inspect.signature(function)

    param_dict = OrderedDict()
    for param_name, param_value in signature.parameters.items():
        default = param_value.default

        if default is inspect.Parameter.empty:
            param_dict[param_name] = EmptyArgument
        else:
            param_dict[param_name] = default

    return param_dict


def inspect_function_default_params(function):
    param_dict = _inspect_function_params(function=function)

    default_param_dict = OrderedDict()
    for param_name, default_value in param_dict.items():
        if default_value is not EmptyArgument:
            default_param_dict[param_name] = default_value

    return default_param_dict


class Argument(object):
    def __init__(self, *args, **kargs):
        pass

    @property
    def optional(self):
        return None

    @property
    def keyword(self):
        return None

    def gen_argument_set(self):
        pass

class ProcessParam(object):
    def __init__(self):
        pass


class Gaussian(object):

    def __init__(self, a, b=2):
        self.a = a
        self.b = b

    @staticmethod
    def meothd_b(a):
        return a + 1

    def method_a(self, a=3):
        return a + self.a


def print_a(*args, **kwargs):
    for i in args:
        print(args)

print(inspect_function_default_params(Gaussian.method_a))