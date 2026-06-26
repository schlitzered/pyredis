from pyredis.commands.base import BaseCommand


class Transaction(BaseCommand):
    """Mixin for Redis Transaction / pipeline commands (e.g. MULTI, EXEC, WATCH)."""

    def __init__(self):
        super().__init__()

    def discard(self, *args, shard_key=None, sock=None):
        if self._cluster:
            return self.execute(
                *[b"DISCARD", *args],
                shard_key=shard_key,
                sock=sock
            )
        return self.execute(
            *[b"DISCARD", *args]
        )

    def exec(self, *args, shard_key=None, sock=None):
        if self._cluster:
            return self.execute(
                *[b"EXEC", *args],
                shard_key=shard_key,
                sock=sock
            )
        return self.execute(
            *[b"EXEC", *args]
        )

    def multi(self, *args, shard_key=None, sock=None):
        if self._cluster:
            return self.execute(
                *[b"MULTI", *args],
                shard_key=shard_key,
                sock=sock
            )
        return self.execute(
            *[b"MULTI", *args]
        )

    def unwatch(self, *args, shard_key=None, sock=None):
        if self._cluster:
            return self.execute(
                *[b"UNWATCH", *args],
                shard_key=shard_key,
                sock=sock
            )
        return self.execute(
            *[b"UNWATCH", *args]
        )

    def watch(self, *args):
        if self._cluster:
            return self.execute(
                *[b"WATCH", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"WATCH", *args]
        )
