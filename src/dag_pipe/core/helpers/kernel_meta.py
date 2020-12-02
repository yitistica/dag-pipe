from collections import OrderedDict

from dag_pipe.core.utils.types import locate_object, check_is_class, check_is_function


def _check_kernel_type(kernel):
    if check_is_function(object_=kernel):
        type_ = 'function'
    elif check_is_class(object_=kernel):
        type_ = 'class'
    elif check_is_method(object_=kernel):
        type_ = 'method'
    else:
        raise TypeError("type is not supported for kernel.")  # TODO custom Error

    return type_


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
