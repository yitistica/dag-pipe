"""
upstream enforcement;
downstream enforcement;

process_b + process_b

Definition of a Process:

same function.

to run a process, requires:
3 main sources:
- input data (could be table, a virtualizer object)
- parameter set (assumed singular);
- configs;


- output:
- validation functions (even validation can be a chain);


when running the process, the process id is generated.

sometimes, the network requires an object,

a task: consists of one or more process:

a task can be compute

job consists of multiple

expose

network material:

expose output;


@Net.register(network=[], input=[], output=[], expose=[], input_process=[], process=[], output_process=[], turn_off=False)
def function():
    pass

only keeps the expose


network.materials[]

"""
import functools


class TaskCore(object):
    def __new__(cls, *args, **kwargs):
        pass

    def __init__(self):
        self._id = None

    @property
    def id(self):
        return self._id


class TaskRunner(object):
    def __init__(self):
        pass

    def process(self):
        pass


class UpStreamProcess(object):
    pass


class DownStreamProcess(object):
    pass


class ProcessInput(object):
    def __init__(self):
        pass

    def validate(self):
        pass


class ProcessResult(object):
    def __init__(self):
        pass


class ProcessData(ProcessInput):
    def __init__(self):
        super().__init__()


class ProcessParameters(ProcessInput):
    def __init__(self):
        super().__init__()


class ProcessNode(object):
    def __init__(self, processor):
        pass

    def _id(self):
        pass

    @property
    def id(self):
        return None

    def _get_predecessors(self):
        pass

    def _set_predecessors(self, predecessors):
        pass

    @property
    def predecessors(self):
        return None

    def run(self):
        pass


def class_register(cls):
    cls._propdict = {}
    for methodname in dir(cls):
        method = getattr(cls, methodname)
        if hasattr(method, '_prop'):
            cls._propdict.update(
                {cls.__name__ + '.' + methodname: method._prop})
    return cls


def register(*args):
    def wrapper(func):
        func._prop = args
        return func
    return wrapper


@class_register
class MyClass(object):

    @register('prop1', 'prop2')
    def my_method(self, arg1, arg2):
        pass

    @register('prop3', 'prop4')
    def my_other_method(self, arg1, arg2):
        pass



