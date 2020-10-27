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

"""


class UpStreamProcess(object):
    pass


class DownStreamProcess(object):
    pass


class ProcessInput(object):
    def __init__(self):
        pass

    def validate(self):
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


class ProcessResult(object):
    def __init__(self):
        pass


