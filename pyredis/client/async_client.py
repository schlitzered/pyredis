from pyredis import commands
from pyredis.connection import AsyncConnection


class AsyncClient(
    commands.Connection,
    commands.Geo,
    commands.Hash,
    commands.HyperLogLog,
    commands.Key,
    commands.List,
    commands.Publish,
    commands.Scripting,
    commands.Set,
    commands.SSet,
    commands.String,
    commands.Transaction,
):
    """
    Asynchronous Redis Client.

    Handles connection lifecycle and command execution asynchronously,
    inheriting all standard Redis command mixins.
    """

    def __init__(self, **kwargs):
        """
        Initialize the AsyncClient connection.

        Args:
            **kwargs: Connection options forwarded to AsyncConnection.
        """
        super().__init__()
        self._conn = AsyncConnection(**kwargs)

    async def execute(self, *args):
        """
        Asynchronously execute a Redis command.

        Args:
            *args: Command name and positional arguments.

        Returns:
            Parsed Redis reply.
        """
        await self._conn.write(*args)
        return await self._conn.read()

    async def close(self):
        """Asynchronously close the underlying connection."""
        await self._conn.close()

    @property
    def closed(self):
        """Flag indicating if connection is closed."""
        return self._conn.closed
