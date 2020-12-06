from collections import OrderedDict

from dag_pipe.core.utils.types import locate_object


def build_function_meta(function_):

    location = locate_object(function_)
    meta = OrderedDict([('location', location)])

    return meta


def build_method_meta(class_, method_name):

    location = locate_object(class_)
    location['method'] = method_name
    meta = OrderedDict([('location', location)])

    return meta


def serialize_kernel_meta(meta):
    meta_str = str(meta)
    return meta_str
