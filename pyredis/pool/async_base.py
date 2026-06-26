import asyncio
from pyredis.exceptions import PyRedisError


class AsyncBasePool(object):
    """
    Base connection pool for asynchronous Redis clients.

    Manages a pool of free and used connections asynchronously, handling acquisition,
    release, and automatic scaling up to the configured pool limit.
    """

    def __init__(
        self,
        database=0,
        password=None,
        encoding=None,
        conn_timeout=2,
        read_timeout=2,
        pool_size=16,
        lock=None,
        username=None,
    ):
        """
        Initialize asynchronous connection pool parameters.

        Args:
            database: Database index to select.
            password: Password for authentication.
            encoding: Optional string encoding for automatic decoding.
            conn_timeout: Async connection timeout in seconds.
            read_timeout: Async read timeout in seconds.
            pool_size: Maximum number of connections allowed in the pool.
            lock: Asyncio lock for synchronization.
            username: Username for ACL authentication.
        """

        self._conn_timeout = conn_timeout
        self._read_timeout = read_timeout
        if lock is None:
            self._lock = asyncio.Lock()
        else:
            self._lock = lock
        self._pool_free = set()
        self._pool_used = set()
        self._database = database
        self._password = password
        self._encoding = encoding
        self._pool_size = pool_size
        self._close_on_err = False
        self._cluster = False
        self._username = username

    @property
    def conn_timeout(self):
        """Async connection timeout in seconds."""
        return self._conn_timeout

    @property
    def read_timeout(self):
        """Async read timeout in seconds."""
        return self._read_timeout

    @property
    def database(self):
        """Database index selected on connections."""
        return self._database

    @property
    def password(self):
        """Authentication password."""
        return self._password

    @property
    def encoding(self):
        """Optional string decoding encoding."""
        return self._encoding

    @property
    def pool_size(self):
        """Maximum number of connections allowed in the pool."""
        return self._pool_size

    @pool_size.setter
    def pool_size(self, size):
        self._pool_size = size
        current_size = len(self._pool_free) + len(self._pool_used)
        while current_size > size:
            try:
                client = self._pool_free.pop()
                asyncio.create_task(
                    client.close()
                )
                current_size -= 1
            except KeyError:
                break

    @property
    def close_on_err(self):
        """Whether to close all idle connections when a connection closes on error."""
        return self._close_on_err

    @property
    def username(self):
        """ACL authentication username."""
        return self._username

    def _connect(self):
        raise NotImplementedError

    async def acquire(self):
        """
        Asynchronously acquire a connection from the pool.

        Reuses an idle connection or establishes a new one if the pool size limit
        has not been reached.

        Returns:
            An AsyncConnection instance.

        Raises:
            PyRedisError: If the maximum pool size is exceeded.
        """
        async with self._lock:
            try:
                client = self._pool_free.pop()
                self._pool_used.add(client)
            except KeyError:
                if len(self._pool_used) < self.pool_size:
                    client = self._connect()
                    if asyncio.iscoroutine(client):
                        client = await client
                    self._pool_used.add(client)
                else:
                    raise PyRedisError(
                        f"Max connections {self.pool_size} exhausted"
                    )
            return client


    async def release(
        self,
        conn
    ):
        """
        Asynchronously release a connection back to the pool.

        Args:
            conn: The AsyncConnection instance to return.
        """
        async with self._lock:
            try:
                current_size = len(self._pool_free) + len(self._pool_used)
                self._pool_used.remove(conn)
                if conn.closed and self.close_on_err:
                    for c in self._pool_free:
                        await c.close()
                    self._pool_free = set()
                    self._pool_used = set()
                elif not conn.closed:
                    if current_size > self.pool_size:
                        await conn.close()
                    else:
                        self._pool_free.add(conn)
            except KeyError:
                await conn.close()


    async def execute(
        self,
        *args,
        **kwargs
    ):
        """
        Asynchronously acquire a connection, execute a command, and release it.

        Args:
            *args: Command name and positional arguments.
            **kwargs: Execution options (e.g. shard_key, sock).

        Returns:
            Parsed Redis reply.
        """
        conn = await self.acquire()
        try:
            return await conn.execute(
                *args,
                **kwargs
            )
        finally:
            await self.release(
                conn=conn
            )

