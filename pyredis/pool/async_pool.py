from pyredis import commands
from pyredis.client import AsyncClient
from pyredis.exceptions import PyRedisError
from pyredis.pool.async_base import AsyncBasePool


class AsyncPool(
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
    def __init__(
        self,
        host=None,
        port=6379,
        unix_sock=None,
        **kwargs
    ):
        if not bool(host) != bool(unix_sock):
            raise PyRedisError("Ether host or unix_sock has to be provided")
        super().__init__(**kwargs)
        self._host = host
        self._port = port
        self._unix_sock = unix_sock

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def unix_sock(self):
        return self._unix_sock

    def _connect(self):
        return AsyncClient(
            host=self.host,
            port=self.port,
            unix_sock=self.unix_sock,
            database=self.database,
            password=self.password,
            encoding=self.encoding,
            conn_timeout=self.conn_timeout,
            read_timeout=self.read_timeout,
            username=self.username,
        )
