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

from dag_pipe.core.utils.types import check_is_iterable
from dag_pipe.core.utils.types import check_container_class


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
    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def add_kwargs(self, **kwargs):
        self._kwargs.update(kwargs)

    @property
    def kwargs(self):
        return self._kwargs


class ArgumentCollection(object):
    def __new__(cls, collection):
        if check_is_iterable(collection):
            self = super().__new__(cls)
        else:
            raise TypeError(f"collection argument takes only an iterable, but was given an {type(collection)}")
        return self

    def __init__(self, collection):
        self.collection = collection

    def __iter__(self):
        return ArgumentCollectionIterator(self)

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


class ArgumentCollectionIterator(object):
    def __new__(cls, argument_collection):
        if isinstance(argument_collection, ArgumentCollection):
            self = super().__new__(cls)
        else:
            raise TypeError(f"argument_collection arg does not support the type: {type(argument_collection)}")
        return self

    def __init__(self, argument_collection):
        self.argument_collection = argument_collection
        self._type = check_container_class(argument_collection.collection)
        self._collection_iterator = None
        self._build_collection_iterator()

    def _build_collection_iterator(self):
        if self._type in (_KEY_ITERABLE_TYPE + _CONTAINER_ITERABLE_TYPE):
            self._collection_iterator = iter(self.argument_collection.collection)
        else:
            raise TypeError(f'type {self._type} is not supported.')

    def __next__(self):
        _next = next(self._collection_iterator)
        if self._type in _KEY_ITERABLE_TYPE:
            return self.argument_collection.collection[_next]
        elif self._type in _CONTAINER_ITERABLE_TYPE:
            return _next
        else:
            raise TypeError(f'type {self._type} is not supported.')


class DefaultArguments(Kwargs):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def if_empty(self):
        if self.kwargs == dict():
            return True
        else:
            return False


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
        self.default_arguments = DefaultArguments()

    def add_default_arguments(self, default_argument_dict):
        self.default_arguments.add_kwargs(**default_argument_dict)

    def _fill_kwargs_with_default(self):
        merged_kwargs = {**self.kwargs}
        for key, default_value in self.default_arguments.kwargs.items():
            if key in self.kwargs:
                pass
            else:
                merged_kwargs[key] = default_value

        return merged_kwargs

    def full_arguments(self):
        args = self.args
        kwargs = self._fill_kwargs_with_default()

        return args, kwargs

    def __iter__(self):
        args, kwargs = self.full_arguments()
        return ArgumentsIterator(args=args, kwargs=kwargs)


class ArgumentsIterator(object):
    def __init__(self, args, kwargs):
        self._args = args
        self._kwargs = kwargs
        self.argument_product = self._build_iterator()

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
            if isinstance(arg_value, ArgumentCollection):
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

        arguments = ArgumentsCore(*args, **kwargs)
        return arguments

    def __next__(self):
        argument_values = next(self.argument_product)
        arguments = self._construct_argument_object_with_values(argument_values=argument_values)
        return arguments


class KernelArguments(Arguments):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_default_arguments_by_function(self, function_):
        default_argument_dict = inspect_function_default_arguments(function_)
        self.add_default_arguments(default_argument_dict=default_argument_dict)
