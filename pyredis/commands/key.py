from pyredis.commands.base import BaseCommand


class Key(BaseCommand):
    """Mixin for Redis Key-level commands (e.g. EXISTS, DEL, EXPIRE, TTL, TYPE)."""

    def __init__(self):
        super().__init__()

    def delete(self, *args):
        if self._cluster:
            return self.execute(
                *[b"DEL", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"DEL", *args]
        )

    def dump(self, *args):
        if self._cluster:
            return self.execute(
                *[b"DUMP", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"DUMP", *args]
        )

    def exists(self, *args):
        if self._cluster:
            return self.execute(
                *[b"EXISTS", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"EXISTS", *args]
        )

    def expire(self, *args):
        if self._cluster:
            return self.execute(
                *[b"EXPIRE", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"EXPIRE", *args]
        )

    def expireat(self, *args):
        if self._cluster:
            return self.execute(b"EXPIREAT")
        return self.execute(
            *[b"EXPIREAT", *args]
        )

    def keys(self, *args, shard_key=None, sock=None):
        if self._cluster:
            return self.execute(
                *[b"KEYS", *args],
                shard_key=shard_key,
                sock=sock
            )
        return self.execute(
            *[b"KEYS", *args]
        )

    def migrate(self, *args):
        if self._cluster:
            raise NotImplementedError
        return self.execute(
            *[b"MIGRATE", *args]
        )

    def move(self, *args):
        if self._cluster:
            return self.execute(
                *[b"MOVE", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"MOVE", *args]
        )

    def object(self, *args, shard_key=None, sock=None):
        if self._cluster:
            return self.execute(
                *[b"DEL", *args],
                shard_key=shard_key,
                sock=sock
            )
        return self.execute(
            *[b"OBJECT", *args]
        )

    def persist(self, *args):
        if self._cluster:
            return self.execute(
                *[b"PERSIST", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"PERSIST", *args]
        )

    def pexpire(self, *args):
        if self._cluster:
            return self.execute(
                *[b"PEXPIRE", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"PEXPIRE", *args]
        )

    def pexpireat(self, *args):
        if self._cluster:
            return self.execute(
                *[b"PEXPIREAT", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"PEXPIREAT", *args]
        )

    def pttl(self, *args):
        if self._cluster:
            return self.execute(
                *[b"PTTL", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"PTTL", *args]
        )

    def randomkey(self, *args, shard_key=None, sock=None):
        if self._cluster:
            return self.execute(
                *[b"RANDOMKEY", *args],
                shard_key=shard_key,
                sock=sock
            )
        return self.execute(
            *[b"RANDOMKEY", *args]
        )

    def rename(self, *args):
        if self._cluster:
            return self.execute(
                *[b"RENAME", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"RENAME", *args]
        )

    def renamenx(self, *args):
        if self._cluster:
            return self.execute(
                *[b"RENAMENX", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"RENAMENX", *args]
        )

    def restore(self, *args):
        if self._cluster:
            return self.execute(
                *[b"RESTORE", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"RESTORE", *args]
        )

    def scan(self, *args, shard_key=None, sock=None):
        if self._cluster:
            return self.execute(
                *[b"SCAN", *args],
                shard_key=shard_key,
                sock=sock
            )
        return self.execute(
            *[b"SCAN", *args]
        )

    def sort(self, *args):
        if self._cluster:
            return self.execute(
                *[b"SORT", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"SORT", *args]
        )

    def ttl(self, *args):
        if self._cluster:
            return self.execute(
                *[b"TTL", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"TTL", *args]
        )

    def type(self, *args):
        if self._cluster:
            return self.execute(
                *[b"TYPE", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"TYPE", *args]
        )

    def wait(self, *args):
        if self._cluster:
            return self.execute(
                *[b"WAIT", *args],
                shard_key=args[0]
            )
        return self.execute(
            *[b"WAIT", *args]
        )
