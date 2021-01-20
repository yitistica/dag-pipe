"""
what arg
base object:
feed can have the value of the collection;
required kernel keywords;

make module

can add repeated argument;

"""
from dag_pipe.helpers.collections.argument import Arguments, DefaultArguments, inspect_function_default_arguments
from dag_pipe.compartment.feed import Feed


class ArgumentValidatorMixin(object):

    def _add_validators_to_args(self, positions, *validators):
        if isinstance(positions, int):
            positions = [positions]
        elif isinstance(positions, (tuple, list, set)) and len(positions) == 0:
            positions = range(len(self.args))
        else:
            pass

        for position in positions:
            self.args[position].add_validators(*validators)

    def _add_validators_to_kwargs(self, keys, *validators):
        if isinstance(keys, (float, int, str)):
            keys = [keys]
        elif isinstance(keys, (tuple, list, set)) and len(keys) == 0:
            keys = self.kwargs.keys()
        for key in keys:
            self.kwargs[key].add_validators(*validators)

    def add_validators(self, positions=(), keys=(), *validators):
        self._add_validators_to_args(positions=positions, *validators)
        self._add_validators_to_kwargs(keys=keys, *validators)


class ProcessArgumentsBase(Arguments, ArgumentValidatorMixin):
    def __init__(self, *args, **kwargs):

        for arg in args:
            if not isinstance(arg, Feed):
                raise TypeError(f'<{arg}> arg of type <{type(arg)}> must be an instance of {Feed}.')

        for key, kwarg in kwargs.items():
            if not isinstance(kwarg, Feed):
                raise TypeError(f'<{key}: {kwarg}> kwarg of type <{type(kwarg)}> must be an instance of {Feed}.')

        super().__init__(*args, **kwargs)

    @property
    def args_values(self):
        args_values = [arg.value for arg in self.args]
        return args_values

    @property
    def kwargs_values(self):
        kwargs_values = {key: kwarg.value for key, kwarg in self.kwargs.items()}
        return kwargs_values

    def _serialize(self):
        # TODO
        pass


class KernelDefaultArguments(DefaultArguments):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_defaults_by_function_inspection(self, function_, only_on=()):
        default_arguments = inspect_function_default_arguments(function_)

        if only_on:
            default_arguments = {key: value for key, value in default_arguments.items() if key in only_on}

        self.add_defaults(**default_arguments)


class KernelArguments(ProcessArgumentsBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.default_arguments = KernelDefaultArguments()

    def full_arguments(self):
        args = self.args
        kwargs = self.kwargs

        return args, kwargs

