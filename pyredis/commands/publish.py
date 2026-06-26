from pyredis.commands.base import BaseCommand


class Publish(BaseCommand):
    def __init__(self):
        super().__init__()

    def publish(self, *args):
        if self._cluster:
            raise NotImplementedError
        return self.execute(
            *[b"PUBLISH", *args]
        )
