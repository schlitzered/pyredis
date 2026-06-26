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
        return self._conn_timeout

    @property
    def read_timeout(self):
        return self._read_timeout

    @property
    def database(self):
        return self._database

    @property
    def password(self):
        return self._password

    @property
    def encoding(self):
        return self._encoding

    @property
    def pool_size(self):
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
        return self._close_on_err

    @property
    def username(self):
        return self._username

    def _connect(self):
        raise NotImplementedError

    async def acquire(self):
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
