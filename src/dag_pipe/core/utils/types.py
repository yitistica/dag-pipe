"""

NOTE ON BOUND AND UNBOUND METHOD:

CAUTION !:
The implementation takes some assumptions that may not be:

is_method:
inspect.ismethod(obj) (Return True if the object is a bound method written in Python):
| method/function          | return |
| :---                     | :----: |
| Class.classmethod        | True   |
| class.staticmethod       | False  |
| class.instancemethod     | False  |
| instance.classmethod     | True   |
| instance.staticmethod    | False  |
| instance.instancemethod  | True   |
| function                 | False  |
"""

import hashlib
import inspect
from collections import OrderedDict
from collections.abc import Iterable
import functools


def _get_object_name(object_):
    return object_.__name__


def _get_object_module_name(object_):
    module = object_.__module__
    return module


def locate_object(object_):
    location = OrderedDict([('module', _get_object_module_name(object_)),
                            ('name', _get_object_name(object_))])

    return location


def check_is_iterable(object_):
    return isinstance(object_, Iterable)


def check_is_class(object_):
    return inspect.isclass(object_)


def get_class_that_defined_method(meth):
    """
    !
    :param meth:
    :return:
    """
    if inspect.ismethod(meth) or \
            (inspect.isbuiltin(meth) and getattr(meth, '__self__', None) is not None) \
            and getattr(meth.__self__, '__class__', None):

        for cls in inspect.getmro(meth.__self__.__class__):
            if meth.__name__ in cls.__dict__:
                return cls
        meth = getattr(meth, '__func__', meth)

    elif inspect.isfunction(meth):
        cls = getattr(inspect.getmodule(meth),
                      meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0],
                      None)
        if isinstance(cls, type):
            return cls

    return getattr(meth, '__objclass__', None)


def _get_class_of_method(method_object):
    pass


def _patch_single_method_class(method_object):
    method_name = method_object.__qualname__.split('.')[-1]
    single_method_class = type('SingleMethod', (object,), {'method': method_object})
    return single_method_class


def is_instance_method(method):
    SingleMethod = _patch_single_method_class(method)
    single_method_instance = SingleMethod()
    print(single_method_instance, 'dfdfdfdf')
    self = getattr(single_method_instance.method, '__self__', None)
    print(self, 'cvcxvxvxcvx')
    if callable(single_method_instance.method) and \
        (single_method_instance.method.__self__ is single_method_instance):
        is_instance_method_ = True
    else:
        is_instance_method_ = False

    return is_instance_method_


def is_class_method(method):
    SingleMethod = _patch_single_method_class(method)

    self = getattr(SingleMethod.method, '__self__', None)
    print(self, 'sdasd')
    print(SingleMethod, 'DFFF')
    if (self is SingleMethod) and isinstance(SingleMethod.method, classmethod):
        is_class_method_ = True
    else:
        is_class_method_ = False

    return is_class_method_


def is_static_method(method):
    SingleMethod = _patch_single_method_class(method)

    self = getattr(SingleMethod.method, '__self__', None)
    if (self is None) and isinstance(SingleMethod.method, staticmethod):
        is_static_method_ = True
    else:
        is_static_method_ = False

    return is_static_method_


def is_class_static_instance_method(method):
    SingleMethod = _patch_single_method_class(method)

    self = getattr(SingleMethod.method, '__self__', None)

    if (self is SingleMethod) and isinstance(SingleMethod.method, classmethod):
        method_type = 'class method'
    elif (self is None) and isinstance(SingleMethod.method, staticmethod):
        method_type = 'static method'
    else:
        single_method_instance = SingleMethod()
        if callable(single_method_instance.method) and \
        (single_method_instance.method.__self__ is single_method_instance):
            method_type = 'instance method'
        else:
            method_type = None

    return method_type


# def check_is_function(object_):
#     if callable(object_) and hasattr(object_, '__call__'):
#         _is_function = True
#     else:
#         _is_function = False
#
#     return _is_function


def check_is_function(object_):
    return inspect.isfunction(object_)


def hash_string(string, precision=7):
    hash_ = int(hashlib.sha256(string.encode('utf-8')).hexdigest(), 16) % (10 ** precision)
    return hash_


