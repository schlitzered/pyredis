from pyredis import commands
import pyredis.client


class AsyncPubSubClient(commands.Subscribe):
    """
    Asynchronous Redis Publish/Subscribe Client.

    Supports channel subscription, unsubscription, pattern-based subscriptions,
    and listening for incoming messages asynchronously.
    """

    def __init__(self, **kwargs):
        self._conn = pyredis.client.AsyncConnection(**kwargs)

    async def close(self):
        await self._conn.close()

    @property
    def closed(self):
        return self._conn.closed

    async def write(self, *args):
        return await self._conn.write(*args)

    async def get(self):
        return await self._conn.read(close_on_timeout=False)
