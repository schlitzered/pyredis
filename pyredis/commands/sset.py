from pyredis.commands.base import BaseCommand


class SSet(BaseCommand):
    def __init__(self):
        super().__init__()

    def zadd(self, *args):
        if self._cluster:
            return self.execute(
                *[b"ZADD", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"ZADD", *args]
        )

    def zcard(self, *args):
        if self._cluster:
            return self.execute(
                *[b"ZCARD", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"ZCARD", *args]
        )

    def zcount(self, *args):
        if self._cluster:
            return self.execute(
                *[b"ZCOUNT", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"ZCOUNT", *args]
        )

    def zincrby(self, *args):
        if self._cluster:
            return self.execute(
                *[b"ZINCRBY", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"ZINCRBY", *args]
        )

    def zinterstore(self, *args):
        if self._cluster:
            return self.execute(
                *[b"ZINTERSTORE", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"ZINTERSTORE", *args]
        )

    def zlexcount(self, *args):
        if self._cluster:
            return self.execute(
                *[b"ZLEXCOUNT", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"ZLEXCOUNT", *args]
        )

    def zrange(self, *args):
        if self._cluster:
            return self.execute(
                *[b"ZRANGE", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"ZRANGE", *args]
        )

    def zrangebylex(self, *args):
        if self._cluster:
            return self.execute(
                *[b"ZRANGEBYLEX", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"ZRANGEBYLEX", *args]
        )

    def zrangebyscore(self, *args):
        if self._cluster:
            return self.execute(
                *[b"ZRANGEBYSCORE", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"ZRANGEBYSCORE", *args]
        )

    def zrank(self, *args):
        if self._cluster:
            return self.execute(
                *[b"ZRANK", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"ZRANK", *args]
        )

    def zrem(self, *args):
        if self._cluster:
            return self.execute(
                *[b"ZREM", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"ZREM", *args]
        )

    def zremrangebylex(self, *args):
        if self._cluster:
            return self.execute(
                *[b"ZREMRANGEBYLEX", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"ZREMRANGEBYLEX", *args]
        )

    def zremrangebyrank(self, *args):
        if self._cluster:
            return self.execute(
                *[b"ZREMRANGEBYRANK", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"ZREMRANGEBYRANK", *args]
        )

    def zremrangebyscrore(self, *args):
        if self._cluster:
            return self.execute(
                *[b"ZREMRANGEBYSCORE", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"ZREMRANGEBYSCORE", *args]
        )

    def zrevrange(self, *args):
        if self._cluster:
            return self.execute(
                *[b"ZREVRANGE", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"ZREVRANGE", *args]
        )

    def zrevrangebylex(self, *args):
        if self._cluster:
            return self.execute(
                *[b"ZREVRANGEBYLEX", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"ZREVRANGEBYLEX", *args]
        )

    def zrevrangebyscore(self, *args):
        if self._cluster:
            return self.execute(
                *[b"ZREVRANGEBYSCORE", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"ZREVRANGEBYSCORE", *args]
        )

    def zrevrank(self, *args):
        if self._cluster:
            return self.execute(
                *[b"ZREVRANK", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"ZREVRANK", *args]
        )

    def zscore(self, *args):
        if self._cluster:
            return self.execute(
                *[b"ZSCORE", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"ZSCORE", *args]
        )

    def zunionstore(self, *args):
        if self._cluster:
            return self.execute(
                *[b"ZUNIONSTORE", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"ZUNIONSTORE", *args]
        )

    def zscan(self, *args):
        if self._cluster:
            return self.execute(
                *[b"ZSCAN", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"ZSCAN", *args]
        )
