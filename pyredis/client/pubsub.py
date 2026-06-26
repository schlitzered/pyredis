from pyredis import commands
import pyredis.client


class PubSubClient(commands.Subscribe):
    """
    Synchronous Redis Publish/Subscribe Client.

    Supports channel subscription, unsubscription, pattern-based subscriptions,
    and listening for incoming messages synchronously.
    """

    def __init__(self, **kwargs):
        """
        Initialize the PubSubClient connection.

        Args:
            **kwargs: Connection options forwarded to Connection.
        """
        self._conn = pyredis.client.Connection(**kwargs)

    def close(self):
        """Close the underlying connection."""
        self._conn.close()

    @property
    def closed(self):
        """Flag indicating if the connection is closed."""
        return self._conn.closed

    def write(self, *args):
        """
        Write a command to the underlying connection.

        Args:
            *args: Command name and arguments.
        """
        return self._conn.write(*args)

    def get(self):
        """
        Read the next message/response from the connection.

        Returns:
            The message or response read from Redis.
        """
        return self._conn.read(close_on_timeout=False)
