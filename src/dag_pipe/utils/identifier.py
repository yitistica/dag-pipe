
import uuid
import hashlib


def hash_string(string, precision=7):
    hash_ = int(hashlib.sha256(string.encode('utf-8')).hexdigest(), 16) % (10 ** precision)
    return hash_


def gen_uuid_4_with_prefix(prefix=None, **kwargs):
    if not prefix:
        prefix = ''
    else:
        prefix = prefix + '_'

    id_ = uuid.uuid4().hex

    full_id = f"{prefix}{id_}"

    if 'precision' in kwargs:
        full_id = hash_string(string=full_id, precision=kwargs['precision'])

    return full_id
