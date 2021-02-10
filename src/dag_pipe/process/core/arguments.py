"""
what arg
base object:
feed can have the value of the collection;
required kernel keywords;

make module

can add repeated argument;


within a feed

argument > value collection > feed

"""
from dag_pipe.helpers.collections.argument import ValueCollection, Arguments, DefaultArguments, \
    inspect_function_default_arguments
from dag_pipe.compartment.feed import Feed


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

    def full_arguments(self, add_default=True):
        args = self.args
        kwargs = self.kwargs

        if add_default:
            kwargs = self.default_arguments.merge(kwargs=kwargs)

        return args, kwargs

    def full_argument_values(self, add_default=True):

        arg_values = self.args_values
        kwarg_values = self.kwargs_values

        if add_default:
            kwarg_values = self.default_arguments.merge(kwargs=kwarg_values)

        return arg_values, kwarg_values
