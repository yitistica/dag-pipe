from dag_pipe.helpers.elemental.attributes import Attributes
from dag_pipe.helpers.collections.containers import ValueCollection
from dag_pipe.utils.identifier import gen_uuid_4_with_prefix, hash_string


_HASH_PRECISION = 6
FEED_ID_VAR_NAME = 'feed_id'


class AttributeFilter(object):
    pass


class FeedMetaAttributes(Attributes):
    def __init__(self, kwargs):
        if FEED_ID_VAR_NAME in kwargs:
            raise KeyError(f"intended attribute contains reserved name {FEED_ID_VAR_NAME}, "
                           f"please rename the attribute.")
        else:
            feed_id = gen_uuid_4_with_prefix(precision=_HASH_PRECISION)
            kwargs = {FEED_ID_VAR_NAME: feed_id, **kwargs}

        super().__init__(kwargs)


class FeedAttributes(Attributes):
    pass


class ResultMetaAttributes(Attributes):
    def __init__(self, kwargs):
        if FEED_ID_VAR_NAME in kwargs:
            raise KeyError(f"intended attribute contains reserved name {FEED_ID_VAR_NAME}, "
                           f"please rename the attribute.")
        else:
            feed_id = gen_uuid_4_with_prefix(precision=_HASH_PRECISION)
            kwargs = {FEED_ID_VAR_NAME: feed_id, **kwargs}

        super().__init__(kwargs)


class ResultAttributes(Attributes):
    pass


def _hash_arg_kwargs(args, kwargs):  # this only make sure that the argument holders have not change;
    ids = []
    for arg in args:
        if isinstance(arg, ValueCollection):
            for element in arg:
                ids.append(element.meta[FEED_ID_VAR_NAME])
        else:
            ids.append(arg.meta[FEED_ID_VAR_NAME])

    for kwarg_name, kwarg in kwargs.items():
        if isinstance(kwarg, ValueCollection):
            for element in kwarg:
                ids.append(element.meta[FEED_ID_VAR_NAME])
        else:
            ids.append(kwarg.meta[FEED_ID_VAR_NAME])

    concat_id = '_'.join(ids)
    hash_ = hash_string(string=concat_id)
    return hash_
