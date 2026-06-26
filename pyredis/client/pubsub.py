from pyredis import commands
import pyredis.client


class PubSubClient(commands.Subscribe):
    """
    Synchronous Redis Publish/Subscribe Client.

    Supports channel subscription, unsubscription, pattern-based subscriptions,
    and listening for incoming messages synchronously.
    """

    def __init__(self, **kwargs):
        self._conn = pyredis.client.Connection(**kwargs)

    def close(self):
        self._conn.close()

    @property
    def closed(self):
        return self._conn.closed

    def write(self, *args):
        return self._conn.write(*args)

    def get(self):
        return self._conn.read(close_on_timeout=False)
