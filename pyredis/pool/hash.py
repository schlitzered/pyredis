import pyredis.pool
from pyredis import commands
from pyredis.pool.base import BasePool


class HashPool(
    BasePool,
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
    Synchronous Redis Hashed Client Connection Pool.

    Acts as a proxy for client commands, leasing a synchronous HashClient
    to route operations across multiple client-side hashing nodes.
    """

    def __init__(self, buckets, **kwargs):
        super().__init__(**kwargs)
        self._buckets = buckets
        self._cluster = True

    @property
    def buckets(self):
        return self._buckets

    def _connect(self):
        return pyredis.pool.HashClient(
            buckets=self.buckets,
            database=self.database,
            password=self.password,
            encoding=self.encoding,
            conn_timeout=self.conn_timeout,
            read_timeout=self.read_timeout,
            username=self.username,
        )
