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
import itertools

from dag_pipe.helpers.collections.containers import ValueCollection


class EmptyArgument(object):
    pass


_KEY_ITERABLE_TYPE = [dict]
_CONTAINER_ITERABLE_TYPE = [list, tuple, set]


def _inspect_function_arguments(function_):
    signature = inspect.signature(function_)

    argument_dict = OrderedDict()
    for argument_key, argument_value in signature.parameters.items():
        default = argument_value.default

        if default is inspect.Parameter.empty:
            argument_dict[argument_key] = EmptyArgument
        else:
            argument_dict[argument_key] = default

    return argument_dict


def inspect_function_default_arguments(function_):
    argument_dict = _inspect_function_arguments(function_=function_)

    default_argument_dict = OrderedDict()
    for argument_key, default_argument_value in argument_dict.items():
        if default_argument_value is not EmptyArgument:
            default_argument_dict[argument_key] = default_argument_value

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
    def __init__(self, **kwargs):  # assuming the order of keys is kept in kwargs;
        """
        :param kwargs:
        the order matter of **kwargs: https://www.python.org/dev/peps/pep-0468/
        """

        self._kwargs = kwargs

    def add_kwargs(self, **kwargs):
        self._kwargs.update(kwargs)

    @property
    def kwargs(self):
        return self._kwargs


class ArgumentsCore(Args, Kwargs):
    def __init__(self, *args, **kwargs):
        Args.__init__(self, *args)
        Kwargs.__init__(self, **kwargs)

    def __repr__(self):
        return f"Arguments({self.args}, {self.kwargs})"

    def __str__(self):
        return f"({self.args}, {self.kwargs})"

    def _compare(self, other):
        pass

    def __eq__(self, other):
        return self._compare(other=other)

    def diff(self, other):
        pass


class Arguments(ArgumentsCore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def full_arguments(self):
        args = self.args
        kwargs = self.kwargs

        return args, kwargs

    def first_arguments(self):
        for index, arguments in enumerate(self):
            return arguments
        return None

    def __iter__(self):
        args, kwargs = self.full_arguments()
        return ArgumentsIterator(args=args, kwargs=kwargs)

    def __len__(self):
        pass


class ArgumentsIterator(object):
    def __init__(self, args, kwargs):
        self._args = args
        self._kwargs = kwargs
        self.argument_product = self._build_iterator()

    def __len__(self):
        pass

    def _flatten_args(self):
        return [{'type': 'arg',
                 'key': index,
                 'value': arg} for index, arg in enumerate(self._args)]

    def _flatten_kwargs(self):
        return [{'type': 'kwarg',
                 'key': key,
                 'value': kwarg} for key, kwarg in self._kwargs.items()]

    def _flatten(self):
        arguments = self._flatten_args() + self._flatten_kwargs()
        return arguments

    @staticmethod
    def _build_iterables_pool(flatten_arguments):

        argument_pool = []
        for arg_info in flatten_arguments:
            arg_value = arg_info['value']
            if isinstance(arg_value, ValueCollection):
                argument_pool.append(arg_value)
            else:
                argument_pool.append((arg_value,))

        return argument_pool

    def _build_iterator(self):
        self._flatten_arguments = self._flatten()

        argument_pool = self._build_iterables_pool(self._flatten_arguments)
        argument_product = itertools.product(*argument_pool)
        return argument_product

    def _construct_argument_object_with_values(self, argument_values):
        args, kwargs = [], {}
        for index, argument_value in enumerate(argument_values):
            argument_type = self._flatten_arguments[index]['type']
            if argument_type == 'arg':
                args.append(argument_value)
            elif argument_type == 'kwarg':
                key = self._flatten_arguments[index]['key']
                kwargs[key] = argument_value
            else:
                NotImplementedError(f'argument type ({argument_type}) is not supported.')

        arguments = Arguments(*args, **kwargs)
        return arguments

    def __next__(self):
        argument_values = next(self.argument_product)
        arguments = self._construct_argument_object_with_values(argument_values=argument_values)
        return arguments


class DefaultArguments(Kwargs):  # does not support collection type;
    def __init__(self, **kwargs):
        super().__init__()
        self.add_defaults(**kwargs)

    def if_empty(self):
        if self.kwargs == dict():
            return True
        else:
            return False

    def add_defaults(self, **defaults):
        self.add_kwargs(**defaults)

    def merge(self, kwargs):
        merged_kwargs = {**kwargs}
        for key, default_value in self.kwargs.items():
            if key in merged_kwargs:
                pass
            else:
                merged_kwargs[key] = default_value

        return merged_kwargs


