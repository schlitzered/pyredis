import pyredis.pool
from pyredis import commands
from pyredis.pool.async_base import AsyncBasePool


class AsyncClusterPool(
    AsyncBasePool,
    commands.Connection,
    commands.Geo,
    commands.Hash,
    commands.HyperLogLog,
    commands.Key,
    commands.List,
    commands.Scripting,
    commands.Set,
    commands.SSet,
    commands.String,
):
    """
    Asynchronous Redis Cluster Connection Pool.

    Acts as a proxy for client commands, leasing an asynchronous AsyncClusterClient
    for cluster-routed operations and releasing it back to the pool asynchronously.
    """

    def __init__(
        self,
        seeds,
        slave_ok=False,
        password=None,
        username=None,
        **kwargs
    ):
        super().__init__(
            password=password,
            **kwargs
        )
        self._map = pyredis.pool.AsyncClusterMap(
            seeds=seeds,
            password=password,
            username=username
        )
        self._slave_ok = slave_ok
        self._cluster = True

    @property
    def slave_ok(self):
        return self._slave_ok

    def _connect(self):
        return pyredis.pool.AsyncClusterClient(
            database=self.database,
            password=self.password,
            encoding=self.encoding,
            slave_ok=self.slave_ok,
            conn_timeout=self.conn_timeout,
            read_timeout=self.read_timeout,
            cluster_map=self._map,
            username=self.username,
        )
