"""
Process = Kernel + argument


what if init twice with different arguments, and based on


for process: if process pool exists the same, must raise?


consider batch operation;  recurrent, or start, node, batch-wise operation,


each process: has a skip process

function: able to loop over a function for x times;



@process.init()  # dependent init, or at start init;
@process.method()
@process.add_preprocessor()
@process.add_afterprocess()  # such as easily convert it into different format;
@process.input()
@process.expose_network()
@process.func(*kernel_args, **kernel_kwargs, analyzer=(func1, func2))


process log:
export to nosql or any database with specificied format, gen table;


process id is different from run time id, process id

"""

from dag_pipe.process.kernels import FunctionKernel, InitKernel, MethodKernel, ClassMethodKernel, StaticMethodKernel
from dag_pipe.process.core.process import ProcessAttributes
from dag_pipe.process.core.arguments import KernelArguments


class KernelNotBuiltError(Exception):
    def __init__(self):
        message = f'Kernel is not built.'
        super().__init__(message)


class ProcessCollection(object):  # TEMP
    Processes = dict()


class ProcessComponent(object):
    pass


class EmptyComponent(object):
    pass


class ProcessCore(object):
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

        if type_ in ['init', 'method', 'classmethod', 'staticmethod']:
            method_name = kwargs.get('method_name')
            if not method_name:
                raise TypeError(f'method_name is not supplied for Kernel of type {type_}.')

            kernel = kernel_cls(class_=callable_, method_name=method_name)
        elif type_ in ['function']:
            kernel = kernel_cls(callable_=callable_)
        else:
            raise TypeError(f'Kernel type {type_} is not supported.')

        process_kernel = super().__new__(cls)
        process_kernel._kernel = kernel
        process_kernel._kernel_type = type_

        return process_kernel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        return self.kernel.callable(*args, **kwargs)


class Process(ProcessCore):
    def __init__(self):
        super().__init__()
        self._kernel = EmptyComponent()
        self._kernel_arguments = KernelArguments()

    def add_kernel(self, callable_, type_):
        self._kernel = ProcessKernel(callable_, type_)

    def add_kernel_arguments(self, *args, **kwargs):
        self._kernel_arguments = KernelArguments(*args, **kwargs)

    def _run_kernel(self, *args, **kwargs):
        if not isinstance(self._kernel, ProcessKernel):
            raise KernelNotBuiltError()
        else:
            self._kernel.run(*args, **kwargs)

    def run_process(self):
        pass


class ProcessRunTime(object):  # separate, some only init once,
    def __init__(self):
        pass


class ProcessLog(object):

    def __init__(self):
        self.occurrence = 0

    def _record_occurence(self):
        self.occurrence += 1

