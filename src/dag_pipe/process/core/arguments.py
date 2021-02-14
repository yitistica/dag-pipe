"""
what arg
base object:
feed can have the value of the collection;
required kernel keywords;

make module

can add repeated argument;


hash individual;

"""
from dag_pipe.helpers.collections.argument import ValueCollection, Arguments, DefaultArguments, \
    inspect_function_default_arguments
from dag_pipe.compartment.feed import Feed
from dag_pipe.utils.identifier import hash_string

_KERNEL_ARGUMENT_INCLUDE_DEFAULT = True
_KERNEL_ARGUMENT_HASH_PRECISION = 7


def _hash_arguments_values(args, kwargs):  # this only make sure that the argument holders have not change;
    ids = []
    for arg in args:
        if isinstance(arg, ValueCollection):
            for element in arg:
                ids.append(str(element.value_id))
        else:
            ids.append(str(arg.value_id))

    for kwarg_name, kwarg in kwargs.items():
        if isinstance(kwarg, ValueCollection):
            for element in kwarg:
                ids.append(str(element.value_id))
        else:
            ids.append(str(kwarg.value_id))

    concat_id = '_'.join(ids)
    hash_ = hash_string(string=concat_id)
    return hash_


class ArgumentValidatorMixin(object):

    @staticmethod
    def _add_validator_to_arg(arg, *validators):
        if isinstance(arg, ValueCollection):
            for element in arg:
                element.add_validators(*validators)
        else:
            arg.add_validators(*validators)

    def _add_validators_to_args(self, positions, *validators):
        if isinstance(positions, int):
            positions = [positions]
        elif isinstance(positions, (tuple, list, set)) and len(positions) == 0:
            positions = range(len(self.args))
        else:
            pass

        for position in positions:
            ArgumentValidatorMixin._add_validator_to_arg(arg=self.args[position], *validators)

    def _add_validators_to_kwargs(self, keys, *validators):
        if isinstance(keys, (float, int, str)):
            keys = [keys]
        elif isinstance(keys, (tuple, list, set)) and len(keys) == 0:
            keys = self.kwargs.keys()
        else:
            raise TypeError(f'keys arg ({keys}) of type {type(keys)}')
        for key in keys:
            ArgumentValidatorMixin._add_validator_to_arg(arg=self.kwargs[key], *validators)

    def add_validators(self, positions=(), keys=(), *validators):
        self._add_validators_to_args(positions=positions, *validators)
        self._add_validators_to_kwargs(keys=keys, *validators)


class ProcessArgumentsBase(Arguments, ArgumentValidatorMixin):
    def __init__(self, *args, **kwargs):

        for arg in args:
            if isinstance(arg, ValueCollection):
                for element in arg:
                    if not isinstance(element, Feed):
                        raise TypeError(f'<{element}> arg of type <{type(element)}> must be an instance of {Feed}.')
            else:
                if not isinstance(arg, Feed):
                    raise TypeError(f'<{arg}> arg of type <{type(arg)}> must be an instance of {Feed}.')

        for key, kwarg in kwargs.items():
            if isinstance(kwarg, ValueCollection):
                for element in kwarg:
                    if not isinstance(element, Feed):
                        raise TypeError(
                            f'<{key}: {kwarg}> kwarg of type <{type(kwarg)}> must be an instance of {Feed}.')
            else:
                if not isinstance(kwarg, Feed):
                    raise TypeError(f'<{key}: {kwarg}> kwarg of type <{type(kwarg)}> must be an instance of {Feed}.')

        super().__init__(*args, **kwargs)

    def _serialize(self):
        # TODO
        pass

    @property
    def arguments_value_id(self):
        args, kwargs = self.full_arguments()
        value_id = _hash_arguments_values(args, kwargs)
        return value_id


class FlatArguments(ProcessArgumentsBase):
    def __init__(self, *args, **kwargs):
        for arg in args:
            if isinstance(arg, ValueCollection):
                raise TypeError(f"Flat argument {arg} does not support ValueCollection type.")

        for key, kwarg in kwargs.items():
            if isinstance(kwarg, ValueCollection):
                raise TypeError(f"Flat argument {kwarg} does not support ValueCollection type.")

        super().__init__(*args, **kwargs)


class KernelDefaultArguments(DefaultArguments):
    def __init__(self, **defaults):
        super().__init__()
        self.add_default(**defaults)

    def add_default(self, **defaults):
        wrapped_kwargs = dict()
        for key, kwarg in defaults.items():
            wrapped_kwargs[key] = Feed(value=kwarg)

        super().add_defaults(**wrapped_kwargs)

    def add_defaults_by_function_inspection(self, function_, only_on=()):
        default_arguments = inspect_function_default_arguments(function_)

        if only_on:
            default_arguments = {key: value for key, value in default_arguments.items() if key in only_on}

        self.add_defaults(**default_arguments)


class KernelArguments(ProcessArgumentsBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._include_default = _KERNEL_ARGUMENT_INCLUDE_DEFAULT
        self.default_arguments = KernelDefaultArguments()

    @property
    def include_default(self):
        return self._include_default

    @include_default.setter
    def include_default(self, value):
        if not isinstance(value, bool):
            raise TypeError(f"value can only be set to bool type.")
        else:
            self._include_default = value

    def full_arguments(self):  # this method will replace the original one and passed into iterator;
        args = self.args
        kwargs = self.kwargs

        if self._include_default:
            kwargs = self.default_arguments.merge(kwargs=kwargs)

        return args, kwargs
