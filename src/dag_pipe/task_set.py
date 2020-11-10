from dag_pipe.core.graph import TaskRegistry
from dag_pipe.core.task import TaskCore
from dag_pipe.core.kernel import check_meta_meta
from dag_pipe.core.utils.types import check_is_function, is_class_static_instance_method, is_class_method, is_instance_method


class ProcessB(object):
    def __init__(self):
        pass

    @classmethod
    def process_c(cls):
        return 5

    def process_a(self, b):
        return 3

    @staticmethod
    def process_d(a):
        return 6

    @property
    def process_e(self):
        return 1


def func_a():
    return 5


print(is_class_method(ProcessB.process_c), 'class')
print(is_instance_method(ProcessB.process_a), 'instance')
print(is_class_static_instance_method(ProcessB.process_d), 'static')
print(is_class_static_instance_method(ProcessB.process_e), 'property')
print(is_class_static_instance_method(func_a), 'func')
