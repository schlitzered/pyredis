from pyredis.commands.base import BaseCommand


class Set(BaseCommand):
    """Mixin for Redis Set (unordered unique collections) commands (e.g. SADD, SREM, SMEMBERS)."""

    def __init__(self):
        super().__init__()

    def sadd(self, *args):
        if self._cluster:
            return self.execute(
                *[b"SADD", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"SADD", *args]
        )

    def scard(self, *args):
        if self._cluster:
            return self.execute(
                *[b"SCARD", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"SCARD", *args]
        )

    def sdiff(self, *args):
        if self._cluster:
            return self.execute(
                *[b"SDIFF", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"SDIFF", *args]
        )

    def sdiffstore(self, *args):
        if self._cluster:
            return self.execute(
                *[b"SDIFFSTORE", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"SDIFFSTORE", *args]
        )

    def sinter(self, *args):
        if self._cluster:
            return self.execute(
                *[b"SINTER", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"SINTER", *args]
        )

    def sinterstore(self, *args):
        if self._cluster:
            return self.execute(
                *[b"SINTERSTORE", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"SINTERSTORE", *args]
        )

    def sismember(self, *args):
        if self._cluster:
            return self.execute(
                *[b"SISMEMBER", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"SISMEMBER", *args]
        )

    def smembers(self, *args):
        if self._cluster:
            return self.execute(
                *[b"SMEMBERS", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"SMEMBERS", *args]
        )

    def smove(self, *args):
        if self._cluster:
            return self.execute(
                *[b"SMOVE", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"SMOVE", *args]
        )

    def spop(self, *args):
        if self._cluster:
            return self.execute(
                *[b"SPOP", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"SPOP", *args]
        )

    def srandmember(self, *args):
        if self._cluster:
            return self.execute(
                *[b"SRANDMEMBER", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"SRANDMEMBER", *args]
        )

    def srem(self, *args):
        if self._cluster:
            return self.execute(
                *[b"SREM", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"SREM", *args]
        )

    def sunion(self, *args):
        if self._cluster:
            return self.execute(
                *[b"SUNION", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"SUNION", *args]
        )

    def sunoinstore(self, *args):
        if self._cluster:
            return self.execute(
                *[b"SUNIONSTORE", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"SUNIONSTORE", *args]
        )

    def sscan(self, *args):
        if self._cluster:
            return self.execute(
                *[b"SSCAN", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"SSCAN", *args]
        )
