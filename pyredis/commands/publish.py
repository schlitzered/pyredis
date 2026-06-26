from pyredis.commands.base import BaseCommand


class Publish(BaseCommand):
    """Mixin for Redis message publishing commands (PUBLISH)."""

    def __init__(self):
        super().__init__()

    def publish(self, *args):
        if self._cluster:
            raise NotImplementedError
        return self.execute(
            *[b"PUBLISH", *args]
        )
