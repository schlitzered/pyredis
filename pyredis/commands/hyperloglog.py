from pyredis.commands.base import BaseCommand


class HyperLogLog(BaseCommand):
    """Mixin for Redis HyperLogLog cardinality estimation commands (e.g. PFADD, PFCOUNT)."""

    def __init__(self):
        super().__init__()

    def pfadd(self, *args):
        if self._cluster:
            return self.execute(
                *[b"PFADD", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"PFADD", *args]
        )

    def pfcount(self, *args):
        if self._cluster:
            return self.execute(
                *[b"PFCOUNT", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"PFCOUNT", *args]
        )

    def pfmerge(self, *args):
        if self._cluster:
            return self.execute(
                *[b"PFMERGE", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"PFMERGE", *args]
        )
