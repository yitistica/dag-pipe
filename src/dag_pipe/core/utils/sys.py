import hashlib
import inspect
from collections import OrderedDict


def _get_object_name(object_):
    return object_.__name__


def _get_object_module(object_):
    module = object_.__module__
    return module


def locate_object(object_):
    location = OrderedDict([('module', _get_object_module(object_)),
                            ('name', _get_object_name(object_))])

    return location


def check_is_class(object_):
    return inspect.isclass(object_)


def check_is_function(object_):
    return inspect.isfunction(object_)


def check_is_method(object_):
    return inspect.ismethod(object_)


def hash_string(string, precision=7):
    hash_ = int(hashlib.sha256(string.encode('utf-8')).hexdigest(), 16) % (10 ** precision)
    return hash_


