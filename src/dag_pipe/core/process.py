"""
Process = Kernel + argument


what if init twice with different arguments, and based on


for process: if process pool exists the same, must raise


consider batch operation;  recurrent init
"""


class ProcessCollection(object):  # TEMP
    Processes = dict()


class ProcessCore(object):
    def __init__(self, kernel):
        self.kernel = kernel
        self._id = None
        self._type = None

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type


class ProcessRun(object):

    def __init__(self):
        self.occurrence = 0

    def _record_occurence(self):
        self.occurrence += 1



class Process(ProcessCore):
    def __init__(self, kernel):
        super().__init__(kernel)





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


class Gaussian(object):

    def __init__(self, a, b=2):
        self.a = a
        self.b = b

    def method_a(self, a=3):
        return a + self.a


Kernel(Gaussian.method_a)

print(KernelCollection.kernels)


Kernel(Gaussian.method_a)

print(KernelCollection.kernels)