from dag_pipe.helpers.collections.argument import Arguments, inspect_function_default_arguments


class KernelArguments(Arguments):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_default_arguments_by_function(self, function_):
        default_argument_dict = inspect_function_default_arguments(function_)
        self.add_default_arguments(default_argument_dict=default_argument_dict)



class ProcessArgumentsSet(object):
    def __init__(self):
        pass