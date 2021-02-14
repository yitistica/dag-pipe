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

