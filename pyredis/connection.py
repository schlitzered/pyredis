from pyredis.exceptions import *
from pyredis.protocol import writer
import socket
try:
    from hiredis import Reader
except ImportError:
    from pyredis.protocol import Reader

__all__ = [
    'Connection'
]


class Connection(object):
    """ Low level client for talking to a Redis Server.

    This class is should not be used directly to talk to a Redis server,
    unless you know what you are doing. In most cases it should be
    sufficient to use one of the Client classes, or one of the Connection Pools.

    :param host:
        Host IP or Name to connect,
        can only be set when unix_sock is None.
    :type host: str

    :param port:
        Port to connect, only used when host is also set.
    :type port: int

    :param unix_sock:
        Unix Socket to connect,
        can only be set when host is None.
    :type unix_sock: str

    :param database:
        Select which db should be used for this connection
    :type database: int

    :param password:
        Password used for authentication. If None, no authentication is done
    :type password: str

    :param encoding:
        Convert result strings with this encoding. If None, no encoding is done.
    :type encoding: str

    :param conn_timeout:
        Connect Timeout.
    :type conn_timeout: float

    :param read_timeout:
        Read Timeout.
    :type read_timeout: float

    :param sentinel:
        If True, authentication and database selection is skipped.
    :type sentinel: bool

    """
    def __init__(
            self,
            host=None,
            port=6379,
            unix_sock=None,
            database=0,
            password=None,
            encoding=None,
            conn_timeout=2,
            read_timeout=2,
            sentinel=False):

        if not bool(host) != bool(unix_sock):
            raise PyRedisError('Ether host or unix_sock has to be provided')
        self._closed = False
        self._conn_timeout = conn_timeout
        self._read_timeout = read_timeout
        self._encoding = encoding
        self._reader = None
        self._sentinel = sentinel
        self._writer = writer
        self._sock = None
        self.host = host
        self.port = port
        self.unix_sock = unix_sock
        self.password = password
        self.database = database

    def _authenticate(self):
        if self._sentinel:
            return
        if self.password:
            self.write('AUTH', self.password)
            try:
                self.read()
            except ReplyError as err:
                self.close()
                raise err

    def _connect(self):
        if self._closed:
            raise PyRedisConnError('Connection Gone')
        if self.host:
            sock = self._connect_inet46()
        else:
            sock = self._connect_unix()
        self._sock = sock
        if self._encoding:
            self._reader = Reader(encoding=self._encoding)
        else:
            self._reader = Reader()
        if not self._sentinel:
            self._authenticate()
            self._setdb()
        self._sock.settimeout(self._read_timeout)

    def _connect_inet46(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self._conn_timeout)
            sock.connect((self.host, self.port))
        except socket.gaierror:
            try:
                sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
                sock.settimeout(self._conn_timeout)
                sock.connect((self.host, self.port))
            except socket.gaierror:
                raise PyRedisConnError('Host is neither a IPv4 or IPv6 address')
        except (
            ConnectionAbortedError,
            ConnectionRefusedError,
            OverflowError,
            socket.timeout,
            OSError
        ) as err:
            self.close()
            raise PyRedisConnError('Could not Connect to {0}:{1}: {2}'.format(
                self.host,
                self.port,
                err
            ))
        return sock

    def _connect_unix(self):
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.settimeout(self._conn_timeout)
            sock.connect(self.unix_sock)
        except (
            ConnectionAbortedError,
            ConnectionRefusedError,
            FileNotFoundError,
            socket.timeout,
            OSError
        ) as err:
            self.close()
            raise PyRedisConnError('Could not Connect to {0}: {1}'.format(
                self.host,
                err
            ))
        return sock

    def _setdb(self):
        if self._sentinel:
            return
        self._sock.settimeout(0.1)
        self.write('SELECT', self.database)
        try:
            self.read()
        except ReplyError as err:
            self.close()
            raise err

    def close(self):
        """ Close Client Connection.

        This closes the underlying socket, and mark the connection as closed.

        :return: None
        """
        if self._sock:
            self._sock.close()
        self._sock = None
        self._reader = None
        self._closed = True

    @property
    def closed(self):
        return self._closed

    def read(self, close_on_timeout=True, raise_on_result_err=True):
        """ Read result from the socket.

        :param close_on_timeout:
            Close the connection after a read timeout
        :type close_on_timeout: book

        :param raise_on_result_err:
            Raise exception on protocol errors
        :type raise_on_result_err: bool

        :return: result, exception
        """
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
            except socket.timeout:
                if close_on_timeout:
                    self.close()
                raise PyRedisConnReadTimeout('Connection timeout while reading')
            except ConnectionResetError:
                self.close()
                raise PyRedisConnError('Connection reset by peer')
            if not data:
                self.close()
                raise PyRedisConnClosed('Connection went away while reading')
            self._reader.feed(data)

    def write(self, *args):
        """ Write commands to socket.

        :param args:
            Accepts a variable number of arguments
        :type args: str, int, float

        :return: None
        """
        if not self._sock:
            self._connect()
        msg = self._writer(*args)
        msg_len = len(msg)
        bytes_sent = 0
        while bytes_sent < msg_len:
            try:
                sent = self._sock.send(msg[bytes_sent:])
            except BrokenPipeError as err:
                self.close()
                raise PyRedisConnError('Connection lost while writing: {0}'.format(err))
            bytes_sent += sent
