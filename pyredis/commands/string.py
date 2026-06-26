from pyredis.commands.base import BaseCommand


class String(BaseCommand):
    """Mixin for Redis String and binary value commands (e.g. GET, SET, INCR, APPEND)."""

    def __init__(self):
        super().__init__()

    def append(self, *args):
        if self._cluster:
            return self.execute(
                *[b"APPEND", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"APPEND", *args]
        )

    def bitcount(self, *args):
        if self._cluster:
            return self.execute(
                *[b"BITCOUNT", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"BITCOUNT", *args]
        )

    def bitfield(self, *args):
        if self._cluster:
            return self.execute(
                *[b"BITFIELD", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"BITFIELD", *args]
        )

    def bitop(self, *args):
        if self._cluster:
            return self.execute(
                *[b"BITOP", *args],
                shard_key=args[1]
            )
        return self.execute(
            *[b"BITOP", *args]
        )

    def bitpos(self, *args):
        if self._cluster:
            return self.execute(
                *[b"BITPOS", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"BITPOS", *args]
        )

    def decr(self, *args):
        if self._cluster:
            return self.execute(
                *[b"DECR", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"DECR", *args]
        )

    def decrby(self, *args):
        if self._cluster:
            return self.execute(
                *[b"DECRBY", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"DECRBY", *args]
        )

    def get(self, *args):
        if self._cluster:
            return self.execute(
                *[b"GET", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"GET", *args]
        )

    def getbit(self, *args):
        if self._cluster:
            return self.execute(
                *[b"GETBIT", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"GETBIT", *args]
        )

    def getrange(self, *args):
        if self._cluster:
            return self.execute(
                *[b"GETRANGE", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"GETRANGE", *args]
        )

    def getset(self, *args):
        if self._cluster:
            return self.execute(
                *[b"GETSET", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"GETSET", *args]
        )

    def incr(self, *args):
        if self._cluster:
            return self.execute(
                *[b"INCR", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"INCR", *args]
        )

    def incrby(self, *args):
        if self._cluster:
            return self.execute(
                *[b"INCRBY", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"INCRBY", *args]
        )

    def incrbyfloat(self, *args):
        if self._cluster:
            return self.execute(
                *[b"INCRBYFLOAT", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"INCRBYFLOAT", *args]
        )

    def mget(self, *args):
        if self._cluster:
            return self.execute(
                *[b"MGET", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"MGET", *args]
        )

    def mset(self, *args):
        if self._cluster:
            return self.execute(
                *[b"MSET", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"MSET", *args]
        )

    def msetnx(self, *args):
        if self._cluster:
            return self.execute(
                *[b"MSETNX", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"MSETNX", *args]
        )

    def psetex(self, *args):
        if self._cluster:
            return self.execute(
                *[b"PSETEX", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"PSETEX", *args]
        )

    def set(self, *args):
        if self._cluster:
            return self.execute(
                *[b"SET", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"SET", *args]
        )

    def setbit(self, *args):
        if self._cluster:
            return self.execute(
                *[b"SETBIT", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"SETBIT", *args]
        )

    def setex(self, *args):
        if self._cluster:
            return self.execute(
                *[b"SETEX", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"SETEX", *args]
        )

    def setnx(self, *args):
        if self._cluster:
            return self.execute(
                *[b"SETNX", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"SETNX", *args]
        )

    def setrange(self, *args):
        if self._cluster:
            return self.execute(
                *[b"SETRANGE", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"SETRANGE", *args]
        )

    def strlen(self, *args):
        if self._cluster:
            return self.execute(
                *[b"STRLEN", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"STRLEN", *args]
        )
