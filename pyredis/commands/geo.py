from pyredis.commands.base import BaseCommand


class Geo(BaseCommand):
    """Mixin for Redis Geo (spatial/geographic) commands (e.g. GEOADD, GEODIST)."""

    def __init__(self):
        super().__init__()

    def geoadd(self, *args):
        if self._cluster:
            return self.execute(
                *[b"GEOADD", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"GEOADD", *args]
        )

    def geodist(self, *args):
        if self._cluster:
            return self.execute(
                *[b"GEODIST", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"GEODIST", *args]
        )

    def geohash(self, *args):
        if self._cluster:
            return self.execute(
                *[b"GEOHASH", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"GEOHASH", *args]
        )

    def georadius(self, *args):
        if self._cluster:
            return self.execute(
                *[b"GEORADIUS", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"GEORADIUS", *args]
        )

    def geopos(self, *args):
        if self._cluster:
            return self.execute(
                *[b"GEOPOS", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"GEOPOS", *args]
        )

    def georadiusbymember(self, *args):
        if self._cluster:
            return self.execute(
                *[b"GEORADIUSBYMEMBER", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"GEORADIUSBYMEMBER", *args]
        )
