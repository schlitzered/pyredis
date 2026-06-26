import threading
from pyredis.exceptions import PyRedisError


class BasePool(object):
    """
    Base connection pool for synchronous Redis clients.

    Manages a pool of free and used connections, handling acquisition, release,
    and automatic scaling up to the configured pool limit.
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
        Initialize connection pool parameters.

        Args:
            database: Database index to select.
            password: Password for authentication.
            encoding: Optional string encoding for automatic decoding.
            conn_timeout: Socket connection timeout in seconds.
            read_timeout: Socket read timeout in seconds.
            pool_size: Maximum number of connections allowed in the pool.
            lock: Threading lock for synchronization.
            username: Username for ACL authentication.
        """

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
        """Socket connection timeout in seconds."""
        return self._conn_timeout

    @property
    def read_timeout(self):
        """Socket read timeout in seconds."""
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
        """Whether to close all idle connections when a connection closes on error."""
        return self._close_on_err

    @property
    def username(self):
        """ACL authentication username."""
        return self._username

    def _connect(self):
        raise NotImplementedError

    def acquire(self):
        """
        Acquire a connection from the pool.

        Reuses an idle connection or establishes a new one if the pool size limit
        has not been reached.

        Returns:
            A Connection instance.

        Raises:
            PyRedisError: If the maximum pool size is exceeded.
        """
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
        """
        Release a connection back to the pool.

        Args:
            conn: The Connection instance to return.
        """
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
        """
        Acquire a connection, execute a command, and release it back to the pool.

        Args:
            *args: Command name and positional arguments.
            **kwargs: Execution options (e.g. shard_key, sock).

        Returns:
            Parsed Redis reply.
        """
        conn = self.acquire()
        try:
            return conn.execute(
                *args,
                **kwargs
            )
        finally:
            self.release(conn)

