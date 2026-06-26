from pyredis import commands
import pyredis.client
from pyredis.exceptions import PyRedisConnError
from pyredis.exceptions import PyRedisError
from pyredis.helper import slot_from_key


class AsyncHashClient(
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
    commands.Transaction,
):
    """
    Asynchronous Redis Client Hashing across multiple buckets.

    Determines connection socket for a command by calculating the keyspace slot from 
    the shard_key and mapping it to one of the configured server buckets asynchronously.
    """

    def __init__(
        self,
        buckets,
        database=None,
        password=None,
        encoding=None,
        conn_timeout=2,
        read_timeout=2,
        username=None,
    ):
        super().__init__()
        self._conns = dict()
        self._conn_names = list()
        self._bulk = False
        self._bulk_keep = False
        self._bulk_results = None
        self._bulk_size = None
        self._bulk_size_current = None
        self._bulk_bucket_order = list()
        self._closed = False
        self._cluster = True
        self._map = dict()
        self._init_conns(
            buckets=buckets,
            database=database,
            password=password,
            encoding=encoding,
            conn_timeout=conn_timeout,
            read_timeout=read_timeout,
            username=username,
        )
        self._init_map()

    async def _bulk_fetch(self):
        for conn in self._bulk_bucket_order:
            result = await conn.read(raise_on_result_err=False)
            if self._bulk_keep:
                self._bulk_results.append(result)
        self._bulk_bucket_order = list()
        self._bulk_size_current = 0

    @staticmethod
    async def _execute_basic(*args, conn):
        await conn.write(*args)
        return await conn.read()

    async def _execute_bulk(self, *args, conn):
        await conn.write(*args)
        self._bulk_size_current += 1
        self._bulk_bucket_order.append(conn)
        if self._bulk_size_current == self._bulk_size:
            await self._bulk_fetch()

    def _init_conns(
        self,
        buckets,
        database,
        password,
        encoding,
        conn_timeout,
        read_timeout,
        username,
    ):
        for bucket in buckets:
            host, port = bucket
            bucketname = f"{host}_{port}"
            self._conn_names.append(bucketname)
            self._conns[bucketname] = pyredis.client.AsyncConnection(
                host=host,
                port=port,
                database=database,
                password=password,
                encoding=encoding,
                conn_timeout=conn_timeout,
                read_timeout=read_timeout,
                username=username,
            )

    def _init_map(self):
        num_buckets = len(self._conn_names) - 1
        cur_bucket = 0
        for slot in range(16384):
            self._map[slot] = self._conn_names[cur_bucket]
            if cur_bucket == num_buckets:
                cur_bucket = 0
            else:
                cur_bucket += 1

    @property
    def bulk(self):
        return self._bulk

    def bulk_start(self, bulk_size=5000, keep_results=True):
        if self.bulk:
            raise PyRedisError("Already in bulk mode")
        self._bulk = True
        self._bulk_size = bulk_size
        self._bulk_size_current = 0
        if keep_results:
            self._bulk_results = []
            self._bulk_keep = True

    async def bulk_stop(self):
        if not self.bulk:
            raise PyRedisError("Not in bulk mode")
        await self._bulk_fetch()
        results = self._bulk_results
        self._bulk = False
        self._bulk_keep = False
        self._bulk_results = None
        self._bulk_size = None
        self._bulk_size_current = None
        return results

    async def close(self):
        for conn in self._conns.values():
            await conn.close()
        self._closed = True

    @property
    def closed(self):
        return self._closed

    async def execute(self, *args, shard_key=None, sock=None):
        if not bool(shard_key) != bool(sock):
            raise PyRedisError("Ether shard_key or sock has to be provided")
        if not sock:
            sock = self._map[slot_from_key(shard_key)]
        conn = self._conns[sock]
        try:
            if not self._bulk:
                return await self._execute_basic(
                    *args,
                    conn=conn
                )
            else:
                await self._execute_bulk(
                    *args,
                    conn=conn
                )
        except PyRedisConnError as err:
            await self.close()
            raise err
