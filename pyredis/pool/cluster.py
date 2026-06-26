import pyredis.pool
from pyredis import commands
from pyredis.pool.base import BasePool


class ClusterPool(
    BasePool,
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
        self._map = pyredis.pool.ClusterMap(
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
        return pyredis.pool.ClusterClient(
            database=self.database,
            password=self.password,
            encoding=self.encoding,
            slave_ok=self.slave_ok,
            conn_timeout=self.conn_timeout,
            read_timeout=self.read_timeout,
            cluster_map=self._map,
            username=self.username,
        )
