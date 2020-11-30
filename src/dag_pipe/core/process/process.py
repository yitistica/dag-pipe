"""
Process = Kernel + argument


what if init twice with different arguments, and based on


for process: if process pool exists the same, must raise


consider batch operation;  recurrent init


each process: has a skip process

function: able to loop over a function for x times;


@process.init()
@process.func(*kernel_args, **kernel_kwargs, analyzer=(func1, func2))
@process.method()


process log:
export to nosql or any database with specificied format, gen table;


process id is different from run time id, process id

"""

from dag_pipe.core.kernel import Kernel, KernelCollection


class ProcessCollection(object):  # TEMP
    Processes = dict()


class ProcessCore(object):
    def __init__(self):
        self._id = None

    @property
    def id(self):
        return self._id  # id should have a runtime difference


class ProcessKernel(object):
    def __init__(self, function, type_):
        self.kernel = Kernel(function)  # check if the process is created
        self._type = type_

    @property
    def kernel_id(self):
        return self.kernel.id


class ProcessParams(object):
    def __init__(self):
        pass


class Process(ProcessCore, ProcessKernel):
    def __init__(self, kernel):
        super().__init__(kernel)


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