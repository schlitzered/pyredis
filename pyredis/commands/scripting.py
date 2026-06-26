from pyredis.commands.base import BaseCommand


class Scripting(BaseCommand):
    def __init__(self):
        super().__init__()

    def eval(self, *args, shard_key=None, sock=None):
        if self._cluster:
            return self.execute(
                *[b"EVAL", *args],
                shard_key=shard_key,
                sock=sock
            )
        return self.execute(
            *[b"EVAL", *args]
        )

    def evalsha(self, *args, shard_key=None, sock=None):
        if self._cluster:
            return self.execute(
                *[b"EVALSHA", *args],
                shard_key=shard_key,
                sock=sock
            )
        return self.execute(
            *[b"EVALSHA", *args]
        )

    def script_debug(self, *args, shard_key=None, sock=None):
        if self._cluster:
            return self.execute(
                *[b"SCRIPT", b"DEBUG", *args],
                shard_key=shard_key,
                sock=sock
            )
        return self.execute(
            *[b"SCRIPT", b"DEBUG", *args]
        )

    def script_exists(self, *args, shard_key=None, sock=None):
        if self._cluster:
            return self.execute(
                *[b"SCRIPT", b"EXISTS", *args],
                shard_key=shard_key,
                sock=sock
            )
        return self.execute(
            *[b"SCRIPT", b"EXISTS", *args]
        )

    def script_flush(self, *args, shard_key=None, sock=None):
        if self._cluster:
            return self.execute(
                *[b"SCRIPT", b"FLUSH", *args],
                shard_key=shard_key,
                sock=sock
            )
        return self.execute(
            *[b"SCRIPT", b"FLUSH", *args]
        )

    def script_kill(self, *args, shard_key=None, sock=None):
        if self._cluster:
            return self.execute(
                *[b"SCRIPT", b"KILL", *args],
                shard_key=shard_key,
                sock=sock
            )
        return self.execute(
            *[b"SCRIPT", b"KILL", *args]
        )

    def script_load(self, *args, shard_key=None, sock=None):
        if self._cluster:
            return self.execute(
                *[b"SCRIPT", b"LOAD", *args],
                shard_key=shard_key,
                sock=sock
            )
        return self.execute(
            *[b"SCRIPT", b"LOAD", *args]
        )
