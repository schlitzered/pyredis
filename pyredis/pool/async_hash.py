import pyredis.pool
from pyredis import commands
from pyredis.pool.async_base import AsyncBasePool


class AsyncHashPool(
    AsyncBasePool,
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
):
    """
    Asynchronous Redis Hashed Client Connection Pool.

    Acts as a proxy for client commands, leasing an asynchronous AsyncHashClient
    to route operations across multiple client-side hashing nodes asynchronously.
    """

    def __init__(self, buckets, **kwargs):
        """
        Initialize the AsyncHashPool connection manager.

        Args:
            buckets: Dict mapping server keyspace slots/buckets to connection options.
            **kwargs: Additional options forwarded to AsyncBasePool.
        """
        super().__init__(**kwargs)
        self._buckets = buckets
        self._cluster = True

    @property
    def buckets(self):
        """Dict of connection options for node buckets."""
        return self._buckets

    def _connect(self):
        return pyredis.pool.AsyncHashClient(
            buckets=self.buckets,
            database=self.database,
            password=self.password,
            encoding=self.encoding,
            conn_timeout=self.conn_timeout,
            read_timeout=self.read_timeout,
            username=self.username,
        )
