import pyredis.connection
from pyredis.exceptions import PyRedisConnClosed
from pyredis.exceptions import PyRedisConnError
from pyredis.exceptions import PyRedisConnReadTimeout
from pyredis.exceptions import PyRedisError
from pyredis.exceptions import ReplyError


class Connection(object):
    """Low level client for talking to a Redis Server."""

    def __init__(
        self,
        host=None,
        port=6379,
        unix_sock=None,
        database=None,
        password=None,
        encoding=None,
        conn_timeout=2,
        read_only=False,
        read_timeout=2,
        sentinel=False,
        username=None,
    ):
        if not bool(host) != bool(unix_sock):
            raise PyRedisError("Ether host or unix_sock has to be provided")
        self._closed = False
        self._conn_timeout = conn_timeout
        self._read_only = read_only
        self._read_timeout = read_timeout
        self._encoding = encoding
        self._reader = None
        self._sentinel = sentinel
        self._writer = pyredis.connection.writer
        self._sock = None
        self.host = host
        self.port = port
        self.unix_sock = unix_sock
        self.password = password
        self.username = username
        self.database = database

    def _authenticate(self):
        if self.username and self.password:
            self.write(
                *["AUTH", self.username, self.password]
            )
            try:
                self.read()
            except ReplyError as err:
                self.close()
                raise err
        elif self.password:
            self.write(
                *["AUTH", self.password]
            )
            try:
                self.read()
            except ReplyError as err:
                self.close()
                raise err

    def _connect(self):
        if self._closed:
            raise PyRedisConnError("Connection Gone")
        if self.host:
            sock = self._connect_inet46()
        else:
            sock = self._connect_unix()
        self._sock = sock
        if self._encoding:
            self._reader = pyredis.connection.Reader(encoding=self._encoding)
        else:
            self._reader = pyredis.connection.Reader()
        self._authenticate()
        if not self._sentinel:
            self._setdb()
            self._set_read_only()
        self._sock.settimeout(self._read_timeout)

    def _connect_inet46(self):
        try:
            sock = pyredis.connection.socket.create_connection(
                address=(self.host, self.port),
                timeout=self._conn_timeout
            )
        except (
            ConnectionAbortedError,
            ConnectionRefusedError,
            OverflowError,
            pyredis.connection.socket.timeout,
            OSError,
        ) as err:
            self.close()
            raise PyRedisConnError(
                f"Could not Connect to {self.host}:{self.port}: {err}"
            )
        return sock

    def _connect_unix(self):
        try:
            sock = pyredis.connection.socket.socket(
                family=pyredis.connection.socket.AF_UNIX,
                type=pyredis.connection.socket.SOCK_STREAM,
            )
            sock.settimeout(self._conn_timeout)
            sock.connect(self.unix_sock)
        except (
            ConnectionAbortedError,
            ConnectionRefusedError,
            FileNotFoundError,
            pyredis.connection.socket.timeout,
            OSError,
        ) as err:
            self.close()
            raise PyRedisConnError(
                f"Could not Connect to {self.host}: {err}"
            )
        return sock

    def _setdb(self):
        if self._sentinel:
            return
        if self.database is None:
            return
        self._sock.settimeout(0.1)
        self.write(
            *["SELECT", self.database]
        )
        try:
            self.read()
        except ReplyError as err:
            self.close()
            raise err

    def _set_read_only(self):
        if self._read_only:
            self.write("READONLY")
            try:
                self.read()
            except ReplyError as err:
                self.close()
                raise err

    def close(self):
        if self._sock:
            self._sock.close()
        self._sock = None
        self._reader = None
        self._closed = True

    @property
    def closed(self):
        return self._closed

    def read(self, close_on_timeout=True, raise_on_result_err=True):
        if not self._sock:
            self._connect()
        while True:
            result = self._reader.gets()
            if result is not False:
                if raise_on_result_err:
                    if isinstance(result, Exception):
                        raise result
                return result
            try:
                data = self._sock.recv(1500)
            except pyredis.connection.socket.timeout:
                if close_on_timeout:
                    self.close()
                raise PyRedisConnReadTimeout(
                    "Connection timeout while reading"
                )
            except ConnectionResetError:
                self.close()
                raise PyRedisConnError("Connection reset by peer")
            if not data:
                self.close()
                raise PyRedisConnClosed("Connection went away while reading")
            self._reader.feed(data)

    def write(self, *args):
        if not self._sock:
            self._connect()
        data = self._writer(*args)
        try:
            self._sock.sendall(data)
        except BrokenPipeError as err:
            self.close()
            raise PyRedisConnError(
                f"Connection lost while writing: {err}"
            )
