import asyncio
from pyredis.exceptions import PyRedisConnClosed
from pyredis.exceptions import PyRedisConnError
from pyredis.exceptions import PyRedisConnReadTimeout
from pyredis.exceptions import PyRedisError
from pyredis.exceptions import ReplyError
import pyredis.connection


class AsyncConnection(object):
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
        self._reader_parser = None
        self._sentinel = sentinel
        self._writer_func = pyredis.connection.writer
        self._reader = None
        self._writer = None
        self.host = host
        self.port = port
        self.unix_sock = unix_sock
        self.password = password
        self.username = username
        self.database = database

    async def _authenticate(self):
        if self.username and self.password:
            await self.write(
                *["AUTH", self.username, self.password]
            )
            try:
                await self.read()
            except ReplyError as err:
                await self.close()
                raise err
        elif self.password:
            await self.write(
                *["AUTH", self.password]
            )
            try:
                await self.read()
            except ReplyError as err:
                await self.close()
                raise err

    async def _connect(self):
        if self._closed:
            raise PyRedisConnError("Connection Gone")
        try:
            if self.host:
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(
                        host=self.host,
                        port=self.port
                    ),
                    timeout=self._conn_timeout
                )
            else:
                reader, writer = await asyncio.wait_for(
                    asyncio.open_unix_connection(
                        path=self.unix_sock
                    ),
                    timeout=self._conn_timeout
                )
        except (
            ConnectionAbortedError,
            ConnectionRefusedError,
            OverflowError,
            asyncio.TimeoutError,
            OSError,
        ) as err:
            await self.close()
            raise PyRedisConnError(
                f"Could not Connect to {self.host}:{self.port}: {err}"
            )
        self._reader = reader
        self._writer = writer
        if self._encoding:
            self._reader_parser = pyredis.connection.Reader(
                encoding=self._encoding
            )
        else:
            self._reader_parser = pyredis.connection.Reader()
        await self._authenticate()
        if not self._sentinel:
            await self._setdb()
            await self._set_read_only()

    async def _setdb(self):
        if self._sentinel:
            return
        if self.database is None:
            return
        await self.write(
            *["SELECT", self.database]
        )
        try:
            await self.read()
        except ReplyError as err:
            await self.close()
            raise err

    async def _set_read_only(self):
        if self._read_only:
            await self.write("READONLY")
            try:
                await self.read()
            except ReplyError as err:
                await self.close()
                raise err

    async def close(self):
        if self._writer:
            self._writer.close()
            try:
                await self._writer.wait_closed()
            except Exception:
                pass
        self._reader = None
        self._writer = None
        self._reader_parser = None
        self._closed = True

    @property
    def closed(self):
        return self._closed

    async def read(self, close_on_timeout=True, raise_on_result_err=True):
        if not self._writer:
            await self._connect()
        while True:
            result = self._reader_parser.gets()
            if result is not False:
                if raise_on_result_err:
                    if isinstance(result, Exception):
                        raise result
                return result
            try:
                data = await asyncio.wait_for(
                    self._reader.read(1500),
                    timeout=self._read_timeout
                )
            except asyncio.TimeoutError:
                if close_on_timeout:
                    await self.close()
                raise PyRedisConnReadTimeout(
                    "Connection timeout while reading"
                )
            except ConnectionResetError:
                await self.close()
                raise PyRedisConnError("Connection reset by peer")
            if not data:
                await self.close()
                raise PyRedisConnClosed("Connection went away while reading")
            self._reader_parser.feed(data)

    async def write(self, *args):
        if not self._writer:
            await self._connect()
        data = self._writer_func(*args)
        try:
            self._writer.write(data)
            await self._writer.drain()
        except BrokenPipeError as err:
            await self.close()
            raise PyRedisConnError(
                f"Connection lost while writing: {err}"
            )
