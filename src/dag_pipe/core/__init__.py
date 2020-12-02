"""
net: a set of processes;
core: a core consists of input:


space: [];
"""

"""
from sth import register, register into which net;

# function.py (external)
def process_a(data, parameter):
    # data must be a regular objects.
    pass
    
# assembling net
from function import process_a

net = Net()
net.set_net_param().import(process_a, data=virtualiser, param=1)
net.import(process_a, data=virtualiser, param=1)

# alternatively: make sure if can be refactored;  (when constructing a project);
@space.import(data=virtualiser, param=1)
def process_a(data):
    pass


when it is called normally, it does not replace anything
"""


def decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper


@decorator
def my_func():
    return 'hello'

