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
from dag_pipe.core.utils.types import check_is_iterable
import inspect


class EmptyArgument(object):
    pass


def _inspect_function_arguments(function):
    signature = inspect.signature(function)

    argument_dict = OrderedDict()
    for param_name, param_value in signature.parameters.items():
        default = param_value.default

        if default is inspect.Parameter.empty:
            argument_dict[param_name] = EmptyArgument
        else:
            argument_dict[param_name] = default

    return argument_dict


def inspect_function_default_arguments(function):
    param_dict = _inspect_function_arguments(function=function)

    default_argument_dict = OrderedDict()
    for param_name, default_value in param_dict.items():
        if default_value is not EmptyArgument:
            default_argument_dict[param_name] = default_value

    return default_argument_dict


class Args(object):
    def __init__(self, *args):
        self._args = args

    def add_args(self, *args):
        self._args = self._args + args

    @property
    def args(self):
        return self._args


class Kwargs(object):
    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def add_kwargs(self, **kwargs):
        self._kwargs.update(kwargs)

    @property
    def kwargs(self):
        return self._kwargs


class Arguments(Args, Kwargs):
    def __init__(self, *args, **kwargs):
        Args.__init__(self, *args)
        Kwargs.__init__(self, **kwargs)


class DefaultArguments(Kwargs):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def if_empty(self):
        if self.kwargs == dict():
            return True
        else:
            return False


class ArgumentCollection(object):
    def __new__(cls, collection):
        if check_is_iterable(collection):
            self = super().__new__(cls)
            self.collection = collection
        else:
            raise TypeError(f"collection argument takes only an iterable, but was given an {type(collection)}")
        return self

    def __repr__(self):
        if hasattr(self.collection, '__repr__'):
            return f"ArgumentCollection({self.collection.__repr__()})"
        else:
            return None

    def __str__(self):
        if hasattr(self.collection, '__str__'):
            return f"ArgumentCollection({self.collection.__str__()})"
        else:
            return None


class KernelArguments(Arguments):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_arguments = DefaultArguments()

    def add_default_arguments(self, default_argument_dict):
        self.default_arguments.add_kwargs(**default_argument_dict)


class ProcessArguments(object):
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


agument = Arguments( w='a', c=[1, 2])

# print(hasattr(range(1,20), '__str__'))

print(ArgumentCollection({'a': 2, 'b': 3}))
# print(inspect_function_default_params(Gaussian.method_a))