__author__ = 'schlitzer'


__all__ = [
    'PyRedisError',
    'PyRedisConnError',
    'PyRedisConnClosed',
    'PyRedisConnReadTimeout',
    'ProtocolError',
    'ReplyError'
]


class PyRedisError(Exception):
    pass


class PyRedisConnError(PyRedisError):
    pass


class PyRedisConnReadTimeout(PyRedisError):
    pass


class PyRedisConnClosed(PyRedisError):
    pass


class ProtocolError(PyRedisError):
    pass


class ReplyError(PyRedisError):
    pass
