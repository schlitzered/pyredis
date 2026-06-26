import pyredis.pool
from pyredis import commands
from pyredis.exceptions import PyRedisError
from pyredis.pool.base import BasePool


class Pool(
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
    Synchronous Redis Connection Pool.

    Acts as a proxy for client commands, lease-acquiring a synchronous connection for
    each command and releasing it back to the pool afterwards.
    """

    def __init__(self, host=None, port=6379, unix_sock=None, **kwargs):
        """
        Initialize the Pool connection manager.

        Args:
            host: Redis server hostname or IP.
            port: Redis server port number.
            unix_sock: Path to Unix domain socket.
            **kwargs: Additional options forwarded to BasePool.
        """
        if not bool(host) != bool(unix_sock):
            raise PyRedisError("Ether host or unix_sock has to be provided")
        super().__init__(**kwargs)
        self._host = host
        self._port = port
        self._unix_sock = unix_sock

    @property
    def host(self):
        """Hostname or IP of the Redis server."""
        return self._host

    @property
    def port(self):
        """Port number of the Redis server."""
        return self._port

    @property
    def unix_sock(self):
        """Path to the Unix domain socket."""
        return self._unix_sock

    def _connect(self):
        return pyredis.pool.Client(
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
