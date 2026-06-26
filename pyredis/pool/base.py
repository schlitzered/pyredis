import threading
from pyredis.exceptions import PyRedisError


class BasePool(object):
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
            self._lock = threading.Lock()
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
        try:
            self._lock.acquire()
            self._pool_size = size
            current_size = len(self._pool_free) + len(self._pool_used)
            while current_size > size:
                try:
                    client = self._pool_free.pop()
                    client.close()
                    current_size -= 1
                except KeyError:
                    break
        finally:
            self._lock.release()

    @property
    def close_on_err(self):
        return self._close_on_err

    @property
    def username(self):
        return self._username

    def _connect(self):
        raise NotImplementedError

    def acquire(self):
        try:
            self._lock.acquire()
            client = self._pool_free.pop()
            self._pool_used.add(client)
        except KeyError:
            if len(self._pool_used) < self.pool_size:
                client = self._connect()
                self._pool_used.add(client)
            else:
                raise PyRedisError(
                    f"Max connections {self.pool_size} exhausted"
                )
        finally:
            self._lock.release()
        return client

    def release(self, conn):
        try:
            self._lock.acquire()
            current_size = len(self._pool_free) + len(self._pool_used)
            self._pool_used.remove(conn)
            if conn.closed and self.close_on_err:
                for c in self._pool_free:
                    c.close()
                self._pool_free = set()
                self._pool_used = set()
            elif not conn.closed:
                if current_size > self.pool_size:
                    conn.close()
                else:
                    self._pool_free.add(conn)
        except KeyError:
            conn.close()
        finally:
            self._lock.release()

    def execute(self, *args, **kwargs):
        conn = self.acquire()
        try:
            return conn.execute(
                *args,
                **kwargs
            )
        finally:
            self.release(conn)
