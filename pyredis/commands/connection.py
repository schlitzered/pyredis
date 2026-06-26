from pyredis.commands.base import BaseCommand


class Connection(BaseCommand):
    """Mixin for Redis Connection commands (e.g. PING, ECHO)."""

    def __init__(self):
        super().__init__()

    def echo(self, *args, shard_key=None, sock=None):
        if self._cluster:
            return self.execute(
                *[b"ECHO", *args],
                shard_key=shard_key,
                sock=sock
            )
        return self.execute(
            *[b"ECHO", *args]
        )

    def ping(self, shard_key=None, sock=None):
        if self._cluster:
            return self.execute(
                b"PING",
                shard_key=shard_key,
                sock=sock
            )
        return self.execute(b"PING")
