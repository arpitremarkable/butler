from collections import namedtuple


def to_namedtuple(obj):
    if hasattr(obj, 'keys'):
        return namedtuple('NamedTuple', obj.keys())(**obj)
    elif hasattr(obj, '__iter__'):
        return namedtuple('NamedTuple', obj)(*obj)
    else:
        raise AssertionError('Only dict type or iter type argument is supported')
