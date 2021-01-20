"""
what arg
base object:
feed;
required kernel keywords;

make module

can add repeated argument;

"""
from collections import OrderedDict

from dag_pipe.helpers.collections.argument import Arguments, DefaultMixin, inspect_function_default_arguments
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
        super().__init__(*args, **kwargs)

    @property
    def args_values(self):
        args_values = [arg.value if isinstance(arg, Feed) else arg for arg in self.args]
        return args_values

    @property
    def kwargs_values(self):
        kwargs_values = {key: kwarg.value if isinstance(kwarg, Feed) else kwarg for key, kwarg in self.kwargs.items()}
        return kwargs_values

    def _serialize(self):
        pass


class KernelArguments(ProcessArgumentsBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.default_arguments = DefaultMixin()

    def add_default_arguments_by_function(self, function_):
        default_argument_dict = inspect_function_default_arguments(function_)
        self.default_arguments.add_kwargs(**default_argument_dict)




class ProcessArguments(object):
    def __init__(self):
        pass


