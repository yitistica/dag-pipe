from dag_pipe.core.graph import TaskRegistry
from dag_pipe.core.task import TaskCore
from dag_pipe.core.kernel import check_kernel_meta


class process_b(object):
    def __init__(self):
        pass

    @TaskRegistry.add_task_decor
    def process_a(self, b):
        return 3


def check_is_method(object_):
    import inspect
    return inspect.ismethod(object_)





