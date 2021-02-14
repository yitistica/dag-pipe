"""
Process = Kernel + argument ?

what if init twice with different arguments, and based on

for process: if process pool exists the same, must raise?

consider batch operation;  recurrent, or start, node, batch-wise operation,

each process: has a skip process

function: able to loop over a function for x times;

@process.init()  # dependent init, or at start init;
@process.method()
@process.add_preprocessor()
@process.add_afterprocess()  # such as easily convert it into different format;
@process.expose_network()
@process.func(*kernel_args, **kernel_kwargs, analyzer=(func1, func2))


process log:
export to nosql or any database with specificied format, gen table;


process id is different from run time id, process id


process.arguments(Placeholder(), a=4, )


argument hash: is not the same as hashing the the actual input;
"""

from dag_pipe.process.core.kernel import FunctionKernel, InitKernel, MethodKernel, ClassMethodKernel, StaticMethodKernel
from dag_pipe.process.core.result import ProcessAttributes
from dag_pipe.process.core.arguments import KernelArguments, FlatArguments


class KernelNotBuiltError(Exception):
    def __init__(self):
        message = f'Kernel is not yet built for the process.'
        super().__init__(message)


class ProcessCollection(object):  # TEMP
    Processes = dict()


class ProcessComponent(object):
    pass


class EmptyComponent(object):
    pass


class ProcessCore(object):
    pass


class EmptyInitKernel(object):
    pass


class ProcessKernel(ProcessComponent):
    def __new__(cls, callable_, type_, *args, **kwargs):
        if type_ == 'function':
            kernel_cls = FunctionKernel
        elif type_ == 'init':
            kernel_cls = InitKernel
        elif type_ == 'method':
            kernel_cls = MethodKernel
        elif type_ == 'classmethod':
            kernel_cls = ClassMethodKernel
        elif type_ == 'staticmethod':
            kernel_cls = StaticMethodKernel
        else:
            raise TypeError(f'Kernel type {type_} is not supported.')

        if type_ in ['method', 'classmethod', 'staticmethod']:
            method_name = kwargs.get('method_name')
            if not method_name:
                raise TypeError(f'method_name is not supplied for Kernel of type {type_}.')
            kernel = kernel_cls(class_=callable_, method_name=method_name)
        elif type_ in ['init']:
            kernel = kernel_cls(class_=callable_)
        elif type_ in ['function']:
            kernel = kernel_cls(callable_=callable_)
        else:
            raise TypeError(f'Kernel type {type_} is not supported.')

        process_kernel = super().__new__(cls)
        process_kernel._kernel = kernel
        process_kernel._kernel_type = type_

        return process_kernel

    def __init__(self, *args, **kwargs):
        super().__init__()

    @property
    def kernel(self):
        return self._kernel

    @property
    def kernel_type(self):
        return self._kernel_type

    @kernel_type.setter
    def kernel_type(self, type_):
        raise NotImplementedError()

    def run(self, *args, **kwargs):
        return self.kernel.call(*args, **kwargs)


class ProcessRunTime(object):  # control what to store, run multiple times?
    def __init__(self):
        pass


class Process(ProcessCore):
    def __init__(self):
        super().__init__()
        self._kernel = EmptyInitKernel()
        self._kernel_arguments = KernelArguments()

    def admit_kernel(self, callable_, type_, **kwargs):
        self._kernel = ProcessKernel(callable_=callable_, type_=type_, **kwargs)

    def add_kernel_arguments(self, *args, **kwargs):
        self._kernel_arguments.add_args(*args)
        self._kernel_arguments.add_kwargs(**kwargs)

    def run_kernel(self, *args, **kwargs):
        if not isinstance(self._kernel, ProcessKernel):
            raise KernelNotBuiltError()
        else:
            raw_results = self._kernel.run(*args, **kwargs)

        return raw_results

    @property
    def include_default(self):
        return self._kernel_arguments.include_default

    @include_default.setter
    def include_default(self, value):
        self._kernel_arguments.include_default = value

    def get_kernel_argument_by_index(self, index):
        pass

    def run_process(self):
        # 1. init run time;

        for argument_index, arguments in enumerate(self._kernel_arguments):
            args, kwargs = arguments  # arguments only manage the container;

            flatten_arguments = FlatArguments(*args, **kwargs)
            argument_hash = flatten_arguments.hash_id

            arg_values = (arg.value for arg in args)
            kwarg_values = {kwarg_name: kwarg_value.value for kwarg_name, kwarg_value in kwargs.items()}

            raw_results = self.run_kernel(*arg_values, **kwarg_values)

        return raw_results


