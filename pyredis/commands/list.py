from pyredis.commands.base import BaseCommand


class List(BaseCommand):
    def __init__(self):
        super().__init__()

    def blpop(self, *args):
        if self._cluster:
            return self.execute(
                *[b"BLPOP", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"BLPOP", *args]
        )

    def brpop(self, *args):
        if self._cluster:
            return self.execute(
                *[b"BRPOP", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"BRPOP", *args]
        )

    def brpoplpush(self, *args):
        if self._cluster:
            return self.execute(
                *[b"BRPOPPUSH", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"BRPOPPUSH", *args]
        )

    def lindex(self, *args):
        if self._cluster:
            return self.execute(
                *[b"LINDEX", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"LINDEX", *args]
        )

    def linsert(self, *args):
        if self._cluster:
            return self.execute(
                *[b"LINSERT", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"LINSERT", *args]
        )

    def llen(self, *args):
        if self._cluster:
            return self.execute(
                *[b"LLEN", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"LLEN", *args]
        )

    def lpop(self, *args):
        if self._cluster:
            return self.execute(
                *[b"LPOP", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"LPOP", *args]
        )

    def lpush(self, *args):
        if self._cluster:
            return self.execute(
                *[b"LPUSH", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"LPUSH", *args]
        )

    def lpushx(self, *args):
        if self._cluster:
            return self.execute(
                *[b"LPUSHX", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"LPUSHX", *args]
        )

    def lrange(self, *args):
        if self._cluster:
            return self.execute(
                *[b"LRANGE", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"LRANGE", *args]
        )

    def lrem(self, *args):
        if self._cluster:
            return self.execute(
                *[b"LREM", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"LREM", *args]
        )

    def lset(self, *args):
        if self._cluster:
            return self.execute(
                *[b"LSET", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"LSET", *args]
        )

    def ltrim(self, *args):
        if self._cluster:
            return self.execute(
                *[b"LTRIM", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"LTRIM", *args]
        )

    def rpop(self, *args):
        if self._cluster:
            return self.execute(
                *[b"RPOP", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"RPOP", *args]
        )

    def rpoplpush(self, *args):
        if self._cluster:
            return self.execute(
                *[b"RPOPLPUSH", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"RPOPLPUSH", *args]
        )

    def rpush(self, *args):
        if self._cluster:
            return self.execute(
                *[b"RPUSH", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"RPUSH", *args]
        )

    def rpushx(self, *args):
        if self._cluster:
            return self.execute(
                *[b"RPUSHX", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"RPUSHX", *args]
        )
