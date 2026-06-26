import pyredis.pool
from pyredis import commands
from pyredis.exceptions import PyRedisConnError
from pyredis.pool.base import BasePool


class SentinelPool(
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
    Synchronous Redis Sentinel Connection Pool.

    Provides automatic discovery and failover-routing of Redis master/slave
    connections using a SentinelClient to resolve host locations.
    """

    def __init__(
        self,
        sentinels,
        name,
        slave_ok=False,
        retries=3,
        sentinel_password=None,
        sentinel_username=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self._sentinel = pyredis.pool.SentinelClient(
            sentinels=sentinels,
            password=sentinel_password,
            username=sentinel_username
        )
        self._name = name
        self._slave_ok = slave_ok
        self._retries = retries
        self._close_on_err = True

    @property
    def slave_ok(self):
        return self._slave_ok

    @property
    def name(self):
        return self._name

    @property
    def retries(self):
        return self._retries

    @property
    def sentinels(self):
        return self._sentinel.sentinels

    def _connect(self):
        for _ in range(self.retries):
            if self.slave_ok:
                client = self._get_slave()
            else:
                client = self._get_master()
            if client:
                return client
        raise PyRedisConnError("Could not connect to Redis")

    def _get_client(self, host, port):
        return pyredis.pool.Client(
            host=host,
            port=port,
            database=self.database,
            password=self.password,
            encoding=self.encoding,
            conn_timeout=self.conn_timeout,
            read_timeout=self.read_timeout,
            username=self.username,
        )

    def _get_master(self):
        candidate = self._sentinel.get_master(self.name)
        host = candidate[b"ip"]
        port = int(candidate[b"port"])
        client = self._get_client(
            host=host,
            port=port
        )
        return client

    def _get_slave(self):
        candidates = []
        for candidate in self._sentinel.get_slaves(self.name):
            candidates.append((candidate[b"ip"], int(candidate[b"port"])))
        pyredis.pool.shuffle(candidates)
        host = candidates[0][0]
        port = int(candidates[0][1])
        client = self._get_client(
            host=host,
            port=port
        )
        return client
