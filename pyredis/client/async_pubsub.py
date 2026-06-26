from pyredis import commands
import pyredis.client


class AsyncPubSubClient(commands.Subscribe):
    """
    Asynchronous Redis Publish/Subscribe Client.

    Supports channel subscription, unsubscription, pattern-based subscriptions,
    and listening for incoming messages asynchronously.
    """

    def __init__(self, **kwargs):
        """
        Initialize the AsyncPubSubClient connection.

        Args:
            **kwargs: Connection options forwarded to AsyncConnection.
        """
        self._conn = pyredis.client.AsyncConnection(**kwargs)

    async def close(self):
        """Close the underlying connection asynchronously."""
        await self._conn.close()

    @property
    def closed(self):
        """Flag indicating if the connection is closed."""
        return self._conn.closed

    async def write(self, *args):
        """
        Write a command to the underlying connection asynchronously.

        Args:
            *args: Command name and arguments.
        """
        return await self._conn.write(*args)

    async def get(self):
        """
        Read the next message/response from the connection asynchronously.

        Returns:
            The message or response read from Redis.
        """
        return await self._conn.read(close_on_timeout=False)
