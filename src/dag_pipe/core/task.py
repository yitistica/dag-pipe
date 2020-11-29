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

Net
Task: multiple processes
Process

@debug
@Net.register(network='str', input=Argument(), output=[], expose=[], turn_off=False, rename='a')
@Net.register(input_process=[])
def function():
    pass

only keeps the expose


network.materials[]


if input is not given, then it is then passed on the arguments at runtime;
"""
import functools


class TaskCore(object):
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






