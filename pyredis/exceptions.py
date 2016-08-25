__author__ = 'schlitzer'


__all__ = [
    'PyRedisError',
    'PyRedisURLError',
    'PyRedisConnError',
    'PyRedisConnClosed',
    'PyRedisConnReadTimeout',
    'ProtocolError',
    'ReplyError'
]


class PyRedisError(Exception):
    pass


class PyRedisURLError(PyRedisError):
    pass


class PyRedisConnError(PyRedisError):
    pass


class PyRedisConnReadTimeout(PyRedisError):
    pass


class PyRedisConnClosed(PyRedisError):
    pass


try:
    from hiredis import ReplyError, ProtocolError
except ImportError:
    class ReplyError(PyRedisError):
        pass


    class ProtocolError(PyRedisError):
        pass
