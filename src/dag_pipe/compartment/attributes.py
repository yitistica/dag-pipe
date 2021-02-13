from dag_pipe.helpers.elemental.attributes import Attributes
from dag_pipe.utils.identifier import gen_uuid_4_with_prefix


_HASH_PRECISION = 6
_FEED_ID_VAR_NAME = '_feed_id'


class AttributeFilter(object):
    pass


class FeedMetaAttributes(Attributes):
    pass


class FeedAttributes(Attributes):
    pass


class ResultMetaAttributes(Attributes):
    def __init__(self, kwargs):
        if _FEED_ID_VAR_NAME in kwargs:
            raise KeyError(f"intended attribute contains reserved name {_FEED_ID_VAR_NAME}, "
                           f"please rename the attribute.")
        else:
            feed_id = gen_uuid_4_with_prefix(precision=_HASH_PRECISION)
            kwargs = {_FEED_ID_VAR_NAME: feed_id, **kwargs}

        super().__init__(kwargs)


class ResultAttributes(Attributes):
    pass
