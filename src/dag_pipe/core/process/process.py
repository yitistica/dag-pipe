"""
Process = Kernel + argument


what if init twice with different arguments, and based on


for process: if process pool exists the same, must raise?


consider batch operation;  recurrent, or start, node, batch-wise operation,


each process: has a skip process

function: able to loop over a function for x times;


@process.init()
@process.method()
@process.add_preprocessor()
@process.func(*kernel_args, **kernel_kwargs, analyzer=(func1, func2))


process log:
export to nosql or any database with specificied format, gen table;


process id is different from run time id, process id

"""

from dag_pipe.core.kernel import Kernel, KernelCollection
from dag_pipe.core.process.argument import KernelArguments


class ProcessCollection(object):  # TEMP
    Processes = dict()


class ProcessComponent(object):
    def __init__(self):
        pass


class EmptyComponent(object):
    pass


class ProcessCore(object):
    def __init__(self):
        self._id = None

    @property
    def id(self):
        return self._id  # id should have a runtime difference


class ProcessKernel(ProcessComponent):
    def __init__(self, function_, kernel_type_):
        super().__init__()
        self.kernel = Kernel(function_)
        self._kernel_type = None

    @property
    def kernel_id(self):
        return self.kernel.id

    @property
    def kernel_type(self):
        return self._kernel_type

    @kernel_type.setter
    def kernel_type(self, type_):
        pass




    def exec(self, *args, **kwargs):
        return self.kernel.callable(*args, **kwargs)


class ProcessArguments(ProcessComponent):
    def __init__(self):
        super().__init__()
        self.kernel_arguments = EmptyComponent()

    def add_kernel_arguments(self, *args, **kwargs):
        self.kernel_arguments = KernelArguments(*args, **kwargs)


class Process(ProcessCore):
    def __init__(self, **kwargs):
        super().__init__()

        self.arguments = ProcessArguments()
        self.kernel = EmptyComponent()






class ProcessRunTime(object):  # separate, some only init once,
    def __init__(self):
        pass


class ProcessLog(object):

    def __init__(self):
        self.occurrence = 0

    def _record_occurence(self):
        self.occurrence += 1


class Gaussian(object):

    def __init__(self, a, b=2):
        self.a = a
        self.b = b

    def method_a(self, a):
        return a + self.a


def add_class(cls):
    if 'a' in KernelCollection.kernels:
        KernelCollection.kernels['b'] = cls  # wrap the class
    else:
        KernelCollection.kernels['a'] = cls
    return cls


Kernel(Gaussian.method_a)

print(KernelCollection.kernels)


Kernel(Gaussian.method_a)

print(KernelCollection.kernels)