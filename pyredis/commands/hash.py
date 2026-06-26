from pyredis.commands.base import BaseCommand


class Hash(BaseCommand):
    """Mixin for Redis Hash commands (e.g. HGET, HSET, HDEL)."""

    def __init__(self):
        super().__init__()

    def hdel(self, *args):
        if self._cluster:
            return self.execute(
                *[b"HDEL", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"HDEL", *args]
        )

    def hexists(self, *args):
        if self._cluster:
            return self.execute(
                *[b"HEXISTS", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"HEXISTS", *args]
        )

    def hget(self, *args):
        if self._cluster:
            return self.execute(
                *[b"HGET", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"HGET", *args]
        )

    def hgetall(self, *args):
        if self._cluster:
            return self.execute(
                *[b"HGETALL", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"HGETALL", *args]
        )

    def hincrby(self, *args):
        if self._cluster:
            return self.execute(
                *[b"HINCRBY", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"HINCRBY", *args]
        )

    def hincrbyfloat(self, *args):
        if self._cluster:
            return self.execute(
                *[b"HINCRBYFLOAT", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"HINCRBYFLOAT", *args]
        )

    def hkeys(self, *args):
        if self._cluster:
            return self.execute(
                *[b"HKEYS", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"HKEYS", *args]
        )

    def hlen(self, *args):
        if self._cluster:
            return self.execute(
                *[b"HLEN", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"HLEN", *args]
        )

    def hmget(self, *args):
        if self._cluster:
            return self.execute(
                *[b"HMGET", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"HMGET", *args]
        )

    def hmset(self, *args):
        if self._cluster:
            return self.execute(
                *[b"HMSET", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"HMSET", *args]
        )

    def hset(self, *args):
        if self._cluster:
            return self.execute(
                *[b"HSET", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"HSET", *args]
        )

    def hsetnx(self, *args):
        if self._cluster:
            return self.execute(
                *[b"HSETNX", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"HSETNX", *args]
        )

    def hstrlen(self, *args):
        if self._cluster:
            return self.execute(
                *[b"HSTRLEN", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"HSTRLEN", *args]
        )

    def hvals(self, *args):
        if self._cluster:
            return self.execute(
                *[b"HVALS", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"HVALS", *args]
        )

    def hscan(self, *args):
        if self._cluster:
            return self.execute(
                *[b"HSCAN", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"HSCAN", *args]
        )
