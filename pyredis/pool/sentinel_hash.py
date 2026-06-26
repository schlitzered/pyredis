import pyredis.pool
from pyredis import commands
from pyredis.exceptions import PyRedisConnError
from pyredis.pool.base import BasePool


class SentinelHashPool(
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
    Synchronous Redis Sentinel-Backed Hashed Connection Pool.

    Combines Sentinel discovery with client-side hashing to route commands across
    multiple master/slave sentinel-monitored clusters synchronously.
    """

    def __init__(
        self,
        sentinels,
        buckets,
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
        self._buckets = buckets
        self._slave_ok = slave_ok
        self._retries = retries
        self._close_on_err = True
        self._cluster = True

    @property
    def slave_ok(self):
        return self._slave_ok

    @property
    def buckets(self):
        return self._buckets

    @property
    def retries(self):
        return self._retries

    @property
    def sentinels(self):
        return self._sentinel.sentinels

    def _connect(self):
        if self.slave_ok:
            client = self._get_slaves()
        else:
            client = self._get_masters()
        if client:
            return client

    def _get_hash_client(self, buckets):
        return pyredis.pool.HashClient(
            buckets=buckets,
            database=self.database,
            password=self.password,
            encoding=self.encoding,
            conn_timeout=self.conn_timeout,
            read_timeout=self.read_timeout,
            username=self.username,
        )

    def _get_master(self, bucket):
        candidate = self._sentinel.get_master(bucket)
        host = candidate[b"ip"].decode("utf8")
        port = int(candidate[b"port"])
        return host, port

    def _get_masters(self):
        buckets = list()
        for bucket in self.buckets:
            _counter = self.retries
            while _counter >= 0:
                _counter -= 1
                _bucket = self._get_master(bucket)
                if _bucket:
                    buckets.append(_bucket)
                    break
                if _counter == 0:
                    raise PyRedisConnError(
                        f"Could not connect to bucket {bucket}"
                    )
        return self._get_hash_client(buckets=buckets)

    def _get_slave(self, bucket):
        candidates = []
        for candidate in self._sentinel.get_slaves(bucket):
            candidates.append((candidate[b"ip"], int(candidate[b"port"])))
        pyredis.pool.shuffle(candidates)
        host = candidates[0][0].decode("utf8")
        port = int(candidates[0][1])
        return host, port

    def _get_slaves(self):
        buckets = list()
        for bucket in self.buckets:
            _counter = self.retries
            while _counter >= 0:
                _counter -= 1
                _bucket = self._get_slave(bucket)
                if _bucket:
                    buckets.append(_bucket)
                    break
                if _counter == 0:
                    raise PyRedisConnError(
                        f"Could not connect to bucket {bucket}"
                    )
        return self._get_hash_client(buckets=buckets)
