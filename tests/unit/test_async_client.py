import asyncio
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

from pyredis import get_by_url
from pyredis.client import AsyncClient
from pyredis.client import AsyncClusterClient
from pyredis.client import AsyncHashClient
from pyredis.client import AsyncPubSubClient
from pyredis.client import AsyncSentinelClient
from pyredis.connection import AsyncConnection
from pyredis.exceptions import PyRedisConnClosed
from pyredis.exceptions import PyRedisConnError
from pyredis.exceptions import PyRedisConnReadTimeout
from pyredis.exceptions import PyRedisError
from pyredis.pool import AsyncPool
from pyredis.pool import AsyncClusterPool
from pyredis.pool import AsyncHashPool
from pyredis.pool import AsyncSentinelPool
from pyredis.pool import AsyncSentinelHashPool


class TestAsyncConnection(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.addCleanup(
            patch.stopall
        )
        self.mock_reader = AsyncMock()
        self.mock_writer = MagicMock()
        self.mock_writer.drain = AsyncMock()

        self.patch_open = patch(
            target="asyncio.open_connection",
            new_callable=AsyncMock
        )
        self.mock_open = self.patch_open.start()
        self.mock_open.return_value = (
            self.mock_reader,
            self.mock_writer
        )

        self.patch_open_unix = patch(
            target="asyncio.open_unix_connection",
            new_callable=AsyncMock
        )
        self.mock_open_unix = self.patch_open_unix.start()
        self.mock_open_unix.return_value = (
            self.mock_reader,
            self.mock_writer
        )

        self.patch_reader_parser = patch(
            target="pyredis.connection.Reader",
            autospec=True
        )
        self.mock_reader_parser_class = self.patch_reader_parser.start()
        self.mock_reader_parser = self.mock_reader_parser_class.return_value

    def test_init_default(self):
        conn = AsyncConnection(
            host="127.0.0.1"
        )
        self.assertEqual(
            first=conn.host,
            second="127.0.0.1"
        )
        self.assertEqual(
            first=conn.port,
            second=6379
        )

    def test_init_invalid(self):
        with self.assertRaises(
            expected_exception=PyRedisError
        ):
            AsyncConnection()

    async def test_connect_and_authenticate(self):
        conn = AsyncConnection(
            host="127.0.0.1",
            password="testpass"
        )
        self.mock_reader_parser.gets.side_effect = [
            False,
            b"OK"
        ]
        self.mock_reader.read.return_value = b"+OK\r\n"

        await conn.write(
            *["PING"]
        )

        self.assertEqual(
            first=self.mock_open.call_args[1],
            second={
                "host": "127.0.0.1",
                "port": 6379
            }
        )

    async def test_read_timeout(self):
        conn = AsyncConnection(
            host="127.0.0.1"
        )
        self.mock_reader_parser.gets.return_value = False
        self.mock_reader.read.side_effect = asyncio.TimeoutError

        with self.assertRaises(
            expected_exception=PyRedisConnReadTimeout
        ):
            await conn.read()

    async def test_read_closed(self):
        conn = AsyncConnection(
            host="127.0.0.1"
        )
        self.mock_reader_parser.gets.return_value = False
        self.mock_reader.read.return_value = b""

        with self.assertRaises(
            expected_exception=PyRedisConnClosed
        ):
            await conn.read()


class TestAsyncClient(IsolatedAsyncioTestCase):
    async def test_execute(self):
        client = AsyncClient(
            host="127.0.0.1"
        )
        client._conn = AsyncMock()
        client._conn.read.return_value = b"PONG"

        res = await client.execute(
            *["PING"]
        )

        self.assertEqual(
            first=res,
            second=b"PONG"
        )
        self.assertEqual(
            first=client._conn.write.call_args[0],
            second=(
                "PING",
            )
        )

    async def test_close(self):
        client = AsyncClient(
            host="127.0.0.1"
        )
        client._conn = AsyncMock()
        await client.close()

        self.assertTrue(
            expr=client._conn.close.called
        )


class TestAsyncPool(IsolatedAsyncioTestCase):
    async def test_pool_acquire_release(self):
        pool = AsyncPool(
            host="127.0.0.1",
            pool_size=2
        )
        mock_client = AsyncMock()
        mock_client.closed = False
        pool._connect = Mock()
        pool._connect.return_value = mock_client

        c1 = await pool.acquire()
        self.assertEqual(
            first=c1,
            second=mock_client
        )
        self.assertEqual(
            first=len(pool._pool_used),
            second=1
        )

        await pool.release(
            conn=c1
        )
        self.assertEqual(
            first=len(pool._pool_used),
            second=0
        )
        self.assertEqual(
            first=len(pool._pool_free),
            second=1
        )

    async def test_pool_execute(self):
        pool = AsyncPool(
            host="127.0.0.1"
        )
        mock_client = AsyncMock()
        mock_client.closed = False
        mock_client.execute.return_value = b"OK"
        pool._connect = Mock()
        pool._connect.return_value = mock_client

        res = await pool.execute(
            *["SET", "foo", "bar"]
        )
        self.assertEqual(
            first=res,
            second=b"OK"
        )


class TestAsyncClusterClient(IsolatedAsyncioTestCase):
    async def test_async_cluster_client(self):
        with patch(
            target="pyredis.client.AsyncClusterMap",
            autospec=True
        ) as mock_map_class:
            mock_map = mock_map_class.return_value
            mock_map.id = "mapid"
            mock_map.get_slot.return_value = "127.0.0.1_6379"

            client = AsyncClusterClient(
                seeds=[("127.0.0.1", 6379)]
            )
            client._conns["127.0.0.1_6379"] = AsyncMock()
            client._conns["127.0.0.1_6379"].read.return_value = b"OK"

            res = await client.execute(
                *["SET", "foo", "bar"],
                shard_key="foo"
            )
            self.assertEqual(
                first=res,
                second=b"OK"
            )

    async def test_async_cluster_pool(self):
        with patch(
            target="pyredis.pool.AsyncClusterMap",
            autospec=True
        ):
            pool = AsyncClusterPool(
                seeds=[("127.0.0.1", 6379)]
            )
            mock_client = AsyncMock()
            mock_client.closed = False
            mock_client.execute.return_value = b"OK"
            pool._connect = Mock()
            pool._connect.return_value = mock_client

            res = await pool.execute(
                *["SET", "foo", "bar"]
            )
            self.assertEqual(
                first=res,
                second=b"OK"
            )


class TestAsyncHashClient(IsolatedAsyncioTestCase):
    async def test_async_hash_client(self):
        client = AsyncHashClient(
            buckets=[("127.0.0.1", 6379)]
        )
        mock_conn = AsyncMock()
        client._conns["127.0.0.1_6379"] = mock_conn
        mock_conn.read.return_value = b"OK"

        res = await client.execute(
            *["SET", "foo", "bar"],
            shard_key="foo"
        )
        self.assertEqual(
            first=res,
            second=b"OK"
        )
        self.assertTrue(
            expr=mock_conn.write.called
        )

    async def test_async_hash_pool(self):
        pool = AsyncHashPool(
            buckets=[("127.0.0.1", 6379)]
        )
        mock_client = AsyncMock()
        mock_client.closed = False
        mock_client.execute.return_value = b"OK"
        pool._connect = Mock()
        pool._connect.return_value = mock_client

        res = await pool.execute(
            *["SET", "foo", "bar"]
        )
        self.assertEqual(
            first=res,
            second=b"OK"
        )


class TestAsyncPubSubClient(IsolatedAsyncioTestCase):
    async def test_async_pubsub_client(self):
        with patch(
            target="pyredis.client.AsyncConnection",
            autospec=True
        ) as mock_conn_class:
            mock_conn = mock_conn_class.return_value
            mock_conn.read.return_value = b"message"

            client = AsyncPubSubClient(
                host="127.0.0.1"
            )
            res = await client.get()
            self.assertEqual(
                first=res,
                second=b"message"
            )
            self.assertEqual(
                first=mock_conn.read.call_args[1],
                second={
                    "close_on_timeout": False
                }
            )

            await client.write(
                *["SUBSCRIBE", "channel"]
            )
            self.assertTrue(
                expr=mock_conn.write.called
            )


class TestAsyncSentinel(IsolatedAsyncioTestCase):
    async def test_async_sentinel_client(self):
        client = AsyncSentinelClient(
            sentinels=[("127.0.0.1", 26379)]
        )
        client._conn = AsyncMock()
        client._conn.read.return_value = [
            b"ip",
            b"127.0.0.1",
            b"port",
            b"6379",
        ]

        master = await client.get_master(
            name="mymaster"
        )
        self.assertEqual(
            first=master,
            second={
                b"ip": b"127.0.0.1",
                b"port": b"6379"
            }
        )

    async def test_async_sentinel_pool(self):
        with patch(
            target="pyredis.pool.AsyncSentinelClient",
            autospec=True
        ) as mock_sentinel_class:
            mock_sentinel = mock_sentinel_class.return_value
            mock_sentinel.get_master.return_value = {
                b"ip": b"127.0.0.1",
                b"port": b"6379"
            }

            pool = AsyncSentinelPool(
                sentinels=[("127.0.0.1", 26379)],
                name="mymaster"
            )
            mock_client = AsyncMock()
            pool._get_client = Mock()
            pool._get_client.return_value = mock_client

            client = await pool._get_master()
            self.assertEqual(
                first=client,
                second=mock_client
            )
            self.assertEqual(
                first=pool._get_client.call_args[1],
                second={
                    "host": b"127.0.0.1",
                    "port": 6379
                }
            )

    async def test_async_sentinel_hash_pool(self):
        with patch(
            target="pyredis.pool.AsyncSentinelClient",
            autospec=True
        ) as mock_sentinel_class:
            mock_sentinel = mock_sentinel_class.return_value
            mock_sentinel.get_master.return_value = {
                b"ip": b"127.0.0.1",
                b"port": b"6379"
            }

            pool = AsyncSentinelHashPool(
                sentinels=[("127.0.0.1", 26379)],
                buckets=[("127.0.0.1", 6379)]
            )
            pool._get_hash_client = Mock()
            mock_hash_client = AsyncMock()
            pool._get_hash_client.return_value = mock_hash_client

            client = await pool._get_masters()
            self.assertEqual(
                first=client,
                second=mock_hash_client
            )
            self.assertEqual(
                first=pool._get_hash_client.call_args[1],
                second={
                    "buckets": [
                        (
                            "127.0.0.1",
                            6379
                        )
                    ]
                }
            )


class TestGetByUrl(IsolatedAsyncioTestCase):
    def test_get_by_url_async(self):
        pool = get_by_url(
            url="redis://127.0.0.1:6379",
            async_client=True
        )
        self.assertIsInstance(
            obj=pool,
            cls=AsyncPool
        )

    def test_get_by_url_cluster_async(self):
        with patch(
            target="pyredis.pool.AsyncClusterMap",
            autospec=True
        ):
            pool = get_by_url(
                url="cluster://127.0.0.1:6379",
                async_client=True
            )
            self.assertIsInstance(
                obj=pool,
                cls=AsyncClusterPool
            )

    def test_get_by_url_sentinel_async(self):
        with patch(
            target="pyredis.pool.AsyncSentinelClient",
            autospec=True
        ):
            pool = get_by_url(
                url="sentinel://127.0.0.1:26379?name=mymaster",
                async_client=True
            )
            self.assertIsInstance(
                obj=pool,
                cls=AsyncSentinelPool
            )


