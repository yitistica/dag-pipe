from dag_pipe.helpers.elemental.attributes import Attributes
from dag_pipe.utils.identifier import gen_uuid_4_with_prefix


_HASH_PRECISION = 6
FEED_ID_VAR_NAME = 'feed_id'
FEED_VALUE_ID_VAR_NAME = 'value_id'


class AttributeFilter(object):
    pass


class EmptyValue(object):
    pass


class FeedMetaAttributes(Attributes):
    def __init__(self, kwargs):
        if FEED_ID_VAR_NAME in kwargs:
            raise KeyError(f"intended attribute contains reserved name {FEED_ID_VAR_NAME}, "
                           f"please rename the attribute.")
        else:
            feed_id = gen_uuid_4_with_prefix(precision=_HASH_PRECISION)
            feed_id_kwargs = {FEED_ID_VAR_NAME: feed_id}
            kwargs = {**feed_id_kwargs, **kwargs}

        super().__init__(kwargs)

    @property
    def feed_id(self):
        return self[FEED_ID_VAR_NAME]


class FeedAttributes(Attributes):
    def __init__(self, kwargs):
        if FEED_VALUE_ID_VAR_NAME in kwargs:
            raise KeyError(f"intended attribute contains reserved name {FEED_VALUE_ID_VAR_NAME}, "
                           f"please rename the attribute.")
        else:
            value_kwargs = {FEED_VALUE_ID_VAR_NAME: EmptyValue}
            kwargs = {**value_kwargs, **kwargs}

        super().__init__(kwargs)

    def assign_value_id(self):
        value_id = gen_uuid_4_with_prefix(precision=_HASH_PRECISION)
        self[FEED_VALUE_ID_VAR_NAME] = value_id

    @property
    def value_id(self):
        return self[FEED_VALUE_ID_VAR_NAME]


class ResultMetaAttributes(Attributes):
    def __init__(self, kwargs):
        if FEED_ID_VAR_NAME in kwargs:
            raise KeyError(f"intended attribute contains reserved name {FEED_ID_VAR_NAME}, "
                           f"please rename the attribute.")
        else:
            feed_id = gen_uuid_4_with_prefix(precision=_HASH_PRECISION)
            feed_id_kwargs = {FEED_ID_VAR_NAME: feed_id}
            kwargs = {**feed_id_kwargs, **kwargs}

        super().__init__(kwargs)


class ResultAttributes(Attributes):
    def __init__(self, kwargs):
        if FEED_VALUE_ID_VAR_NAME in kwargs:
            raise KeyError(f"intended attribute contains reserved name {FEED_VALUE_ID_VAR_NAME}, "
                           f"please rename the attribute.")
        else:
            value_kwargs = {FEED_VALUE_ID_VAR_NAME: EmptyValue}
            kwargs = {**value_kwargs, **kwargs}

        super().__init__(kwargs)

    def assign_value_id(self):
        value_id = gen_uuid_4_with_prefix(precision=_HASH_PRECISION)
        self[FEED_VALUE_ID_VAR_NAME] = value_id

    @property
    def value_id(self):
        return self[FEED_VALUE_ID_VAR_NAME]
