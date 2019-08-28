__author__ = 'schlitzer'

from unittest import TestCase
from unittest.mock import Mock, MagicMock, PropertyMock, call, patch

from collections import deque

import pyredis.client
from pyredis.exceptions import *

try:
    from hiredis import ReplyError
except ImportError:
    from pyredis.exceptions import ReplyError


class TestClientUnit(TestCase):
    def setUp(self):
        self.addCleanup(patch.stopall)

        connection_patcher = patch('pyredis.client.Connection', autospec=True)
        self.connection_mock = connection_patcher.start()

    def test___init___args_host__conn(self):
        conn_mock = Mock()
        self.connection_mock.return_value = conn_mock

        client = pyredis.client.Client(host='127.0.0.1')
        self.assertEqual(client._conn, conn_mock)
        self.connection_mock.assert_called_with(
            host='127.0.0.1')

    def test__bulk_fetch(self):
        conn_mock = Mock()
        conn_mock.read.return_value = b'PONG'
        self.connection_mock.return_value = conn_mock

        client = pyredis.client.Client(host='127.0.0.1')
        client._bulk_keep = True
        client._bulk_results = []
        client._bulk_size_current = 3

        client._bulk_fetch()
        conn_mock.read.assert_has_calls([
            call(raise_on_result_err=False),
            call(raise_on_result_err=False),
            call(raise_on_result_err=False)
        ])
        self.assertEqual(client._bulk_results, [b'PONG', b'PONG', b'PONG'])

    def test__execute_basic(self):
        conn_mock = Mock()
        conn_mock.read.return_value = b'PONG'
        self.connection_mock.return_value = conn_mock

        client = pyredis.client.Client(host='127.0.0.1')
        result = client._execute_basic('Ping')
        conn_mock.write.assert_called_with('Ping')
        conn_mock.read.assert_called_with()
        self.assertEqual(result, b'PONG')

    def test__execute_bulk_bulk_size_not_reached(self):
        conn_mock = Mock()
        self.connection_mock.return_value = conn_mock

        client = pyredis.client.Client(host='127.0.0.1')
        client.bulk_start()
        result = client._execute_bulk('Ping')
        conn_mock.write.assert_called_with('Ping')
        self.assertIsNone(result)

    def test__execute_bulk_bulk_size_reached(self):
        conn_mock = Mock()
        conn_mock.read.return_value = b'PONG'
        self.connection_mock.return_value = conn_mock

        client = pyredis.client.Client(host='127.0.0.1')
        client.bulk_start(3)
        result = client._execute_bulk('Ping')
        self.assertIsNone(result)
        self.assertEqual(client._bulk_size_current, 1)
        self.assertEqual(client._bulk_results, [])
        result = client._execute_bulk('Ping')
        self.assertIsNone(result)
        self.assertEqual(client._bulk_size_current, 2)
        self.assertEqual(client._bulk_results, [])
        result = client._execute_bulk('Ping')
        self.assertIsNone(result)
        self.assertEqual(client._bulk_size_current, 0)
        self.assertEqual(client._bulk_results, [b'PONG', b'PONG', b'PONG'])

    def test_execute_non_bulk(self):
        client = pyredis.client.Client(host='127.0.0.1')
        client._execute_basic = Mock()
        client._execute_basic.return_value = b'PONG'

        result = client.execute('Ping')
        client._execute_basic.assert_called_with('Ping')
        self.assertEqual(result, b'PONG')

    def test_bulk(self):
        client = pyredis.client.Client(host='127.0.0.1')
        self.assertEqual(client.bulk, client._bulk)

    def test_bulk_start(self):
        client = pyredis.client.Client(host='127.0.0.1')
        client.bulk_start()
        self.assertTrue(client.bulk)
        self.assertEqual(client._bulk_size, 5000)
        self.assertEqual(client._bulk_size_current, 0)
        self.assertEqual(client._bulk_results, [])
        self.assertTrue(client._bulk_keep)

    def test_bulk_start_no_keep_results(self):
        client = pyredis.client.Client(host='127.0.0.1')
        client.bulk_start(keep_results=False)
        self.assertTrue(client.bulk)
        self.assertEqual(client._bulk_size, 5000)
        self.assertEqual(client._bulk_size_current, 0)
        self.assertIsNone(client._bulk_results)
        self.assertFalse(client._bulk_keep)

    def test_bulk_start_bulk_size_42(self):
        client = pyredis.client.Client(host='127.0.0.1')
        client.bulk_start(bulk_size=42)
        self.assertTrue(client.bulk)
        self.assertEqual(client._bulk_size, 42)
        self.assertEqual(client._bulk_size_current, 0)

    def test_bulk_start_raise_already_open(self):
        client = pyredis.client.Client(host='127.0.0.1')
        client.bulk_start()
        self.assertRaises(PyRedisError, client.bulk_start)

    def test_bulk_stop(self):
        client = pyredis.client.Client(host='127.0.0.1')
        client._bulk_fetch = Mock()
        client._bulk = True
        client._bulk_results = [b'PONG']
        result = client.bulk_stop()
        client._bulk_fetch.assert_called_with()
        self.assertEqual(result, [b'PONG'])
        self.assertFalse(client._bulk)
        self.assertFalse(client._bulk_keep)
        self.assertIsNone(client._bulk_results)
        self.assertIsNone(client._bulk_size)
        self.assertIsNone(client._bulk_size_current)

    def test_bulk_stop_not_in_bulk_mode(self):
        client = pyredis.client.Client(host='127.0.0.1')
        self.assertRaises(PyRedisError, client.bulk_stop)

    def test_closed(self):
        client = pyredis.client.Client(host='127.0.0.1')
        self.assertEqual(client.closed, client._conn.closed)

    def test_execute(self):
        client = pyredis.client.Client(host='127.0.0.1')
        client._execute_basic = Mock()
        client._execute_basic.return_value = b'PONG'
        result = client.execute(b'PING')
        client._execute_basic.assert_called_with(b'PING')
        self.assertEqual(result, b'PONG')

    def test_execute_bulk(self):
        client = pyredis.client.Client(host='127.0.0.1')
        client._execute_bulk = Mock()
        client._bulk = True
        client.execute(b'PING')
        client._execute_bulk.assert_called_with(b'PING')


class TestHashClientUnit(TestCase):
    def setUp(self):
        self.addCleanup(patch.stopall)

        connection_patcher = patch('pyredis.client.Connection', autospec=True)
        self.buckets = [('localhost', 7001), ('localhost', 7002), ('localhost', 7003)]
        self.connection_mock = connection_patcher.start()

    def test___init___args_host__conn(self):
        conn_mock_1 = Mock()
        conn_mock_2 = Mock()
        conn_mock_3 = Mock()
        self.connection_mock.side_effect = [conn_mock_1, conn_mock_2, conn_mock_3]

        client = pyredis.client.HashClient(buckets=self.buckets)

        self.assertEqual(client._conn_names, ['localhost_7001', 'localhost_7002', 'localhost_7003'])
        self.connection_mock.assert_has_calls([
            call(host='localhost', port=7001, conn_timeout=2, database=0, encoding=None, password=None, read_timeout=2),
            call(host='localhost', port=7002, conn_timeout=2, database=0, encoding=None, password=None, read_timeout=2),
            call(host='localhost', port=7003, conn_timeout=2, database=0, encoding=None, password=None, read_timeout=2)
        ])
        self.assertEqual(client._map[0], 'localhost_7001')
        self.assertEqual(client._map[1], 'localhost_7002')
        self.assertEqual(client._map[2], 'localhost_7003')
        self.assertEqual(client._map[3], 'localhost_7001')
        self.assertEqual(client._map[4], 'localhost_7002')
        self.assertEqual(client._map[5], 'localhost_7003')

    def test__bulk_fetch(self):
        conn_mock_1 = Mock()
        conn_mock_1.read.return_value = b'PONG1'
        conn_mock_2 = Mock()
        conn_mock_2.read.return_value = b'PONG2'
        conn_mock_3 = Mock()
        conn_mock_3.read.return_value = b'PONG3'
        self.connection_mock.side_effect = [conn_mock_1, conn_mock_2, conn_mock_3]

        client = pyredis.client.HashClient(buckets=self.buckets)
        client._bulk_keep = True
        client._bulk_results = []
        client._bulk_size_current = 3
        client._bulk_bucket_order.append(conn_mock_1)
        client._bulk_bucket_order.append(conn_mock_2)
        client._bulk_bucket_order.append(conn_mock_3)

        client._bulk_fetch()
        conn_mock_1.read.assert_has_calls([
            call(raise_on_result_err=False),
        ])
        conn_mock_2.read.assert_has_calls([
            call(raise_on_result_err=False),
        ])
        conn_mock_3.read.assert_has_calls([
            call(raise_on_result_err=False),
        ])
        self.assertEqual(client._bulk_results, [b'PONG1', b'PONG2', b'PONG3'])
        self.assertEqual(client._bulk_size_current, 0)
        self.assertEqual(client._bulk_bucket_order, [])

    def test__execute_basic(self):
        conn_mock_1 = Mock()
        conn_mock_1.read.return_value = b'PONG1'
        conn_mock_2 = Mock()
        conn_mock_2.read.return_value = b'PONG2'
        conn_mock_3 = Mock()
        conn_mock_3.read.return_value = b'PONG3'
        self.connection_mock.side_effect = [conn_mock_1, conn_mock_2, conn_mock_3]

        client = pyredis.client.HashClient(buckets=self.buckets)

        result = client._execute_basic('Ping', conn=conn_mock_1)
        conn_mock_1.write.assert_called_with('Ping')
        conn_mock_1.read.assert_called_with()
        self.assertEqual(result, b'PONG1')

    def test__execute_bulk_bulk_size_not_reached(self):
        conn_mock_1 = Mock()
        conn_mock_2 = Mock()
        conn_mock_3 = Mock()
        self.connection_mock.side_effect = [conn_mock_1, conn_mock_2, conn_mock_3]

        client = pyredis.client.HashClient(buckets=self.buckets)
        client.bulk_start()
        result = client._execute_bulk('Ping', conn=conn_mock_1)
        conn_mock_1.write.assert_called_with('Ping')
        self.assertIsNone(result)

    def test__execute_bulk_bulk_size_reached(self):
        conn_mock_1 = Mock()
        conn_mock_1.read.return_value = b'PONG1'
        conn_mock_2 = Mock()
        conn_mock_2.read.return_value = b'PONG2'
        conn_mock_3 = Mock()
        conn_mock_3.read.return_value = b'PONG3'
        self.connection_mock.side_effect = [conn_mock_1, conn_mock_2, conn_mock_3]

        client = pyredis.client.HashClient(buckets=self.buckets)
        client.bulk_start(3)
        result = client._execute_bulk('Ping', conn=conn_mock_1)
        self.assertIsNone(result)
        self.assertEqual(client._bulk_size_current, 1)
        self.assertEqual(client._bulk_results, [])
        result = client._execute_bulk('Ping', conn=conn_mock_2)
        self.assertIsNone(result)
        self.assertEqual(client._bulk_size_current, 2)
        self.assertEqual(client._bulk_results, [])
        result = client._execute_bulk('Ping', conn=conn_mock_3)
        self.assertIsNone(result)
        self.assertEqual(client._bulk_size_current, 0)
        self.assertEqual(client._bulk_results, [b'PONG1', b'PONG2', b'PONG3'])

    def test_execute_non_bulk_shard_key(self):
        conn_mock_1 = Mock()
        conn_mock_2 = Mock()
        conn_mock_3 = Mock()
        self.connection_mock.side_effect = [conn_mock_1, conn_mock_2, conn_mock_3]

        client = pyredis.client.HashClient(buckets=self.buckets)
        client._execute_basic = Mock()
        client._execute_basic.return_value = b'PONG'

        result = client.execute('Ping', shard_key='blarg')
        client._execute_basic.assert_called_with('Ping', conn=conn_mock_3)
        self.assertEqual(result, b'PONG')

    def test_bulk(self):
        conn_mock_1 = Mock()
        conn_mock_2 = Mock()
        conn_mock_3 = Mock()
        self.connection_mock.side_effect = [conn_mock_1, conn_mock_2, conn_mock_3]

        client = pyredis.client.HashClient(buckets=self.buckets)
        self.assertEqual(client.bulk, client._bulk)

    def test_bulk_start(self):
        conn_mock_1 = Mock()
        conn_mock_2 = Mock()
        conn_mock_3 = Mock()
        self.connection_mock.side_effect = [conn_mock_1, conn_mock_2, conn_mock_3]

        client = pyredis.client.HashClient(buckets=self.buckets)
        client.bulk_start()
        self.assertTrue(client.bulk)
        self.assertEqual(client._bulk_size, 5000)
        self.assertEqual(client._bulk_size_current, 0)
        self.assertEqual(client._bulk_results, [])
        self.assertTrue(client._bulk_keep)

    def test_bulk_start_no_keep_results(self):
        conn_mock_1 = Mock()
        conn_mock_2 = Mock()
        conn_mock_3 = Mock()
        self.connection_mock.side_effect = [conn_mock_1, conn_mock_2, conn_mock_3]

        client = pyredis.client.HashClient(buckets=self.buckets)
        client.bulk_start(keep_results=False)
        self.assertTrue(client.bulk)
        self.assertEqual(client._bulk_size, 5000)
        self.assertEqual(client._bulk_size_current, 0)
        self.assertIsNone(client._bulk_results)
        self.assertFalse(client._bulk_keep)

    def test_bulk_start_bulk_size_42(self):
        conn_mock_1 = Mock()
        conn_mock_2 = Mock()
        conn_mock_3 = Mock()
        self.connection_mock.side_effect = [conn_mock_1, conn_mock_2, conn_mock_3]

        client = pyredis.client.HashClient(buckets=self.buckets)
        client.bulk_start(bulk_size=42)
        self.assertTrue(client.bulk)
        self.assertEqual(client._bulk_size, 42)
        self.assertEqual(client._bulk_size_current, 0)

    def test_bulk_start_raise_already_open(self):
        conn_mock_1 = Mock()
        conn_mock_2 = Mock()
        conn_mock_3 = Mock()
        self.connection_mock.side_effect = [conn_mock_1, conn_mock_2, conn_mock_3]

        client = pyredis.client.HashClient(buckets=self.buckets)
        client.bulk_start()
        self.assertRaises(PyRedisError, client.bulk_start)

    def test_bulk_stop(self):
        conn_mock_1 = Mock()
        conn_mock_2 = Mock()
        conn_mock_3 = Mock()
        self.connection_mock.side_effect = [conn_mock_1, conn_mock_2, conn_mock_3]

        client = pyredis.client.HashClient(buckets=self.buckets)
        client._bulk_fetch = Mock()
        client._bulk = True
        client._bulk_results = [b'PONG']
        result = client.bulk_stop()
        client._bulk_fetch.assert_called_with()
        self.assertEqual(result, [b'PONG'])
        self.assertFalse(client._bulk)
        self.assertFalse(client._bulk_keep)
        self.assertIsNone(client._bulk_results)
        self.assertIsNone(client._bulk_size)
        self.assertIsNone(client._bulk_size_current)

    def test_bulk_stop_not_in_bulk_mode(self):
        conn_mock_1 = Mock()
        conn_mock_2 = Mock()
        conn_mock_3 = Mock()
        self.connection_mock.side_effect = [conn_mock_1, conn_mock_2, conn_mock_3]

        client = pyredis.client.HashClient(buckets=self.buckets)
        self.assertRaises(PyRedisError, client.bulk_stop)

    def test_close(self):
        conn_mock_1 = Mock()
        conn_mock_2 = Mock()
        conn_mock_3 = Mock()
        self.connection_mock.side_effect = [conn_mock_1, conn_mock_2, conn_mock_3]

        client = pyredis.client.HashClient(buckets=self.buckets)
        client.close()
        self.assertTrue(client.closed)

    def test_execute(self):
        conn_mock_1 = Mock()
        conn_mock_2 = Mock()
        conn_mock_3 = Mock()
        self.connection_mock.side_effect = [conn_mock_1, conn_mock_2, conn_mock_3]

        client = pyredis.client.HashClient(buckets=self.buckets)
        client._execute_basic = Mock()
        client._execute_basic.return_value = b'PONG'
        result = client.execute(b'PING', shard_key='blarg')
        client._execute_basic.assert_called_with(b'PING', conn=conn_mock_3)
        self.assertEqual(result, b'PONG')

    def test_execute_bulk(self):
        conn_mock_1 = Mock()
        conn_mock_2 = Mock()
        conn_mock_3 = Mock()
        self.connection_mock.side_effect = [conn_mock_1, conn_mock_2, conn_mock_3]

        client = pyredis.client.HashClient(buckets=self.buckets)
        client._execute_bulk = Mock()
        client._bulk = True
        client.execute(b'PING', shard_key='blarg')
        client._execute_bulk.assert_called_with(b'PING', conn=conn_mock_3)


class TestPubSubClientUnit(TestCase):
    def setUp(self):
        self.addCleanup(patch.stopall)

        connection_patcher = patch('pyredis.client.Connection', autospec=True)
        self.connection_mock = connection_patcher.start()

        self.connection_mock_inst = Mock()
        self.connection_mock.return_value = self.connection_mock_inst

        self.client = pyredis.client.PubSubClient(host='localhost')

    def test___init__(self):
        self.assertEqual(self.client._conn, self.connection_mock_inst)
        self.connection_mock.assert_called_with(
            host='localhost')

    def test_get(self):
        self.connection_mock_inst.read.return_value = 'something'

        result = self.client.get()
        self.connection_mock_inst.read.assert_called_with(close_on_timeout=False)
        self.assertEqual(result, 'something')

    def test_write(self):
        self.connection_mock_inst.write.return_value = None

        result = self.client.write()
        self.assertIsNone(result)


class TestSentinelClientUnit(TestCase):
    def setUp(self):
        self.addCleanup(patch.stopall)

        connection_patcher = patch('pyredis.client.Connection', autospec=True)
        self.connection_mock = connection_patcher.start()

        dict_from_list_patcher = patch('pyredis.client.dict_from_list')
        self.dict_from_list_mock = dict_from_list_patcher.start()

    def test___init__(self):
        sentinels = [('host1', 12345), ('host2', 12345), ('host3', 12345)]
        client = pyredis.client.SentinelClient(sentinels=sentinels)
        self.assertEqual(client.sentinels, deque(sentinels))
        self.assertIsNone(client._conn)

    def test__sentinel_connect(self):
        conn_mock = Mock()
        self.connection_mock.return_value = conn_mock
        sentinels = [('host1', 12345), ('host2', 12345), ('host3', 12345)]
        client = pyredis.client.SentinelClient(sentinels=sentinels, password='blubber')
        client.execute = Mock()

        self.assertTrue(client._sentinel_connect(sentinel=('host1', 12345)))
        self.connection_mock.assert_called_with(
            host='host1', port=12345, conn_timeout=0.1, sentinel=True, password='blubber')
        client.execute.assert_called_with('PING')
        self.assertEqual(client._conn, conn_mock)

    def test__sentinel_connect_conn_exception(self):
        conn_mock = Mock()
        self.connection_mock.return_value = conn_mock
        sentinels = [('host1', 12345), ('host2', 12345), ('host3', 12345)]
        client = pyredis.client.SentinelClient(sentinels=sentinels)
        client.close = Mock()
        client.execute = Mock()
        client.execute.side_effect = PyRedisConnError

        self.assertFalse(client._sentinel_connect(sentinel=('host1', 12345)))
        self.connection_mock.assert_called_with(
            host='host1', port=12345, conn_timeout=0.1, sentinel=True, password=None)
        client.execute.assert_called_with('PING')
        client.close.assert_called_with()

    def test__sentinel_get(self):
        sentinels = [('host1', 12345), ('host2', 12345), ('host3', 12345)]
        client = pyredis.client.SentinelClient(sentinels=sentinels)
        client._sentinel_connect = Mock()
        client._conn = True

        client._sentinel_get()
        self.assertEqual(client.sentinels, deque(sentinels))
        client._sentinel_connect.assert_called_with(('host1', 12345))

    def test__sentinel_get_one_connect_err(self):
        sentinels = [('host1', 12345), ('host2', 12345), ('host3', 12345)]
        client = pyredis.client.SentinelClient(sentinels=sentinels)
        client._sentinel_connect = Mock()
        client._sentinel_connect.side_effect = (None, True)

        client._sentinel_get()
        roteted_sentinel = deque(sentinels)
        roteted_sentinel.rotate(-1)
        self.assertEqual(client.sentinels, roteted_sentinel)
        client._sentinel_connect.assert_has_calls([
            call(('host1', 12345)),
            call(('host2', 12345))
        ])

    def test__sentinel_get_one_connect_exhausted(self):
        sentinels = [('host1', 12345), ('host2', 12345), ('host3', 12345)]
        client = pyredis.client.SentinelClient(sentinels=sentinels)
        client._sentinel_connect = Mock()
        client._sentinel_connect.side_effect = (None, None, None)

        self.assertRaises(PyRedisConnError, client._sentinel_get)
        roteted_sentinel = deque(sentinels)
        roteted_sentinel.rotate(-3)
        self.assertEqual(client.sentinels, roteted_sentinel)
        client._sentinel_connect.assert_has_calls([
            call(('host1', 12345)),
            call(('host2', 12345)),
            call(('host3', 12345))
        ])

    def test_close(self):
        sentinels = [('host1', 12345), ('host2', 12345), ('host3', 12345)]
        client = pyredis.client.SentinelClient(sentinels=sentinels)
        client._sentinel_connect = Mock()
        conn_mock = Mock()
        client._conn = conn_mock
        client.close()
        conn_mock.close.assert_called_with()
        self.assertIsNone(client._conn)

    def test_execute(self):
        sentinels = [('host1', 12345), ('host2', 12345), ('host3', 12345)]
        client = pyredis.client.SentinelClient(sentinels=sentinels)
        client._conn = Mock()
        client._conn.read.return_value = b'PONG'
        result = client.execute('PING')
        client._conn.write.assert_called_with('PING')
        client._conn.read.assert_called_with()
        self.assertEqual(result, b'PONG')

    def test_get_master(self):
        dict_expected = {
            "host": "localhost",
            "port": "12345"
        }
        list_expected = ["host", "localhost", "port", "12345"]
        sentinels = [('host1', 12345), ('host2', 12345), ('host3', 12345)]
        client = pyredis.client.SentinelClient(sentinels=sentinels)
        client.execute = Mock()
        client.execute.return_value = list_expected
        self.dict_from_list_mock.return_value = dict_expected
        result = client.get_master('master')
        client.execute.assert_called_with('SENTINEL', 'master', 'master')
        self.dict_from_list_mock.assert_called_with(list_expected)
        self.assertEqual(result, dict_expected)

    def test_get_masters(self):
        dict_result = [
            {
                "host": "localhost",
                "port": "12345"
            },
            {
                "host": "localhost",
                "port": "54321"
            }
        ]
        dict_expected1 = {
            "host": "localhost",
            "port": "12345"
        }
        dict_expected2 = {
            "host": "localhost",
            "port": "54321"
        }
        list_execute = [["host", "localhost", "port", "12345"], ["host", "localhost", "port", "54321"]]
        list_expected1 = ["host", "localhost", "port", "12345"]
        list_expected2 = ["host", "localhost", "port", "54321"]
        sentinels = [('host1', 12345), ('host2', 12345), ('host3', 12345)]
        client = pyredis.client.SentinelClient(sentinels=sentinels)
        client.execute = Mock()
        client.execute.return_value = list_execute
        self.dict_from_list_mock.side_effect = [dict_expected1, dict_expected2]
        result = client.get_masters()
        client.execute.assert_called_with('SENTINEL', 'masters')
        self.dict_from_list_mock.assert_has_calls([
            call(list_expected1),
            call(list_expected2)
        ]
        )
        self.assertEqual(result, dict_result)

    def test_get_slaves(self):
        dict_result = [
            {
                "host": "localhost",
                "port": "12345"
            },
            {
                "host": "localhost",
                "port": "54321"
            }
        ]
        dict_expected1 = {
            "host": "localhost",
            "port": "12345"
        }
        dict_expected2 = {
            "host": "localhost",
            "port": "54321"
        }
        list_execute = [["host", "localhost", "port", "12345"], ["host", "localhost", "port", "54321"]]
        list_expected1 = ["host", "localhost", "port", "12345"]
        list_expected2 = ["host", "localhost", "port", "54321"]
        sentinels = [('host1', 12345), ('host2', 12345), ('host3', 12345)]
        client = pyredis.client.SentinelClient(sentinels=sentinels)
        client.execute = Mock()
        client.execute.return_value = list_execute
        self.dict_from_list_mock.side_effect = [dict_expected1, dict_expected2]
        result = client.get_slaves('mymaster')
        client.execute.assert_called_with('SENTINEL', 'slaves', 'mymaster')
        self.dict_from_list_mock.assert_has_calls([
            call(list_expected1),
            call(list_expected2)
        ])
        self.assertEqual(result, dict_result)

    def test_next_sentinel(self):
        sentinels = [('host1', 12345), ('host2', 12345), ('host3', 12345)]
        expected = deque(sentinels)
        expected.rotate(-1)
        client = pyredis.client.SentinelClient(sentinels=sentinels)
        client. close = Mock()
        client.next_sentinel()
        client.close.assert_called_with()
        self.assertEqual(client.sentinels, expected)


class TestClusterClientUnit(TestCase):
    def setUp(self):
        self.addCleanup(patch.stopall)

        connection_patcher = patch('pyredis.client.Connection', autospec=True)
        self.connection_mock = connection_patcher.start()

        clustermap_patcher = patch('pyredis.client.ClusterMap', autospec=True)
        self.clustermap_mock = clustermap_patcher.start()

        self.clustermap_inst = Mock()

        self.clustermap_mock.return_value = self.clustermap_inst

        self.seeds = [('host1', 12345), ('host2', 12345), ('host3', 12345)]
        self.client = pyredis.client.ClusterClient(seeds=self.seeds)

    def test___init__seeds(self):
        self.clustermap_mock.assert_called_with(seeds=self.seeds)
        self.assertEqual(self.client._map_id, self.clustermap_inst.id)

    def test___init__map(self):
        map = Mock()
        client = pyredis.client.ClusterClient(cluster_map=map)
        self.assertEqual(client._map, map)
        self.assertEqual(client._map_id, map.id)

    def test___init__map_and_seeds(self):
        map = Mock()
        self.assertRaises(
            PyRedisError,
            pyredis.client.ClusterClient,
            seeds=self.seeds,
            cluster_map=map
        )

    def test__cleanup_conns(self):
        conn1_12345 = Mock()
        conn2_12345 = Mock()
        conn3_12345 = Mock()
        self.client._conns['conn1_12345'] = conn1_12345
        self.client._conns['conn2_12345'] = conn2_12345
        self.client._conns['conn3_12345'] = conn3_12345

        self.client._map.hosts.return_value = set(['conn1_12345', 'conn3_12345'])

        self.client._cleanup_conns()

        self.assertTrue(conn2_12345.close.called)
        self.assertFalse(conn1_12345.close.called)
        self.assertFalse(conn3_12345.close.called)
        self.assertNotIn('conn2_12345', self.client._conns)
        self.assertIn('conn1_12345', self.client._conns)
        self.assertIn('conn3_12345', self.client._conns)

    def test__connect(self):
        sock = 'conn1_12345'

        conn = Mock()
        self.connection_mock.return_value = conn

        self.client._connect(sock=sock)

        self.assertEqual(self.client._conns[sock], conn)
        self.connection_mock.assert_called_with(
            host='conn1', port=12345,
            conn_timeout=self.client._conn_timeout,
            read_only=self.client._slave_ok,
            read_timeout=self.client._read_timeout,
            encoding=self.client._encoding,
            password=self.client._password,
            database=self.client._database,
        )

    def test__get_slot_info(self):
        self.client._map_id = 42
        self.client._map.id = 42
        self.client._map.get_slot.return_value = 'host1_12345'

        self.client._cleanup_conns = Mock()

        result = self.client._get_slot_info(shard_key='testkey')

        self.assertEqual(result, 'host1_12345')
        self.assertFalse(self.client._cleanup_conns.called)

    def test__get_slot_info_map_changed(self):
        self.client._map_id = 23
        self.client._map.id = 42
        self.client._map.get_slot.return_value = 'host1_12345'

        self.client._cleanup_conns = Mock()

        result = self.client._get_slot_info(shard_key='testkey')

        self.assertEqual(result, 'host1_12345')
        self.assertTrue(self.client._cleanup_conns.called)
        self.assertEqual(self.client._map_id, 42)

    def test__get_slot_info_key_error(self):
        self.client._map_id = 42
        self.client._map.id = 42
        self.client._map.update.return_value = 23
        self.client._map.get_slot.side_effect = [KeyError, 'host1_12345']

        self.client._cleanup_conns = Mock()

        result = self.client._get_slot_info(shard_key='testkey')

        self.assertEqual(result, 'host1_12345')
        self.assertTrue(self.client._cleanup_conns.called)
        self.assertEqual(self.client._map_id, 23)

    def test_closed(self):
        self.assertFalse(self.client.closed)

    def test_execute_sock_not_connected(self):
        self.client._get_slot_info = Mock()
        self.client._get_slot_info.return_value = 'host1_12345'
        conn = Mock()
        conn.read.return_value = 'success'
        self.connection_mock.return_value = conn

        result = self.client.execute('GET', 'test', shard_key='test')
        self.assertEqual(result, 'success')
        conn.write.assert_called_with('GET', 'test')

    def test_execute_sock_connected(self):
        self.client._get_slot_info = Mock()
        self.client._get_slot_info.return_value = 'host1_12345'
        conn = Mock()
        conn.read.return_value = 'success'

        self.client._conns['host1_12345'] = conn
        self.client._connect = Mock()

        result = self.client.execute('GET', 'test', shard_key='test')
        self.assertEqual(result, 'success')
        conn.write.assert_called_with('GET', 'test')

    def test_execute_ReplyError_ASK(self):
        self.client._get_slot_info = Mock()
        self.client._get_slot_info.return_value = 'host1_12345'
        conn1 = Mock()
        conn1.read.side_effect = [ReplyError('ASK 42 host2:12345')]
        conn2 = Mock()
        conn2.read.side_effect = ['success']
        self.connection_mock.side_effect = [conn1, conn2]

        result = self.client.execute('GET', 'test', shard_key='test')
        self.assertEqual(result, 'success')
        conn1.write.assert_called_with('GET', 'test')
        conn2.write.assert_called_with('ASKING', 'GET', 'test')

    def test_execute_ReplyError_MOVED(self):
        self.client._get_slot_info = Mock()
        self.client._get_slot_info.side_effect = ['host1_12345', 'host2_12345']
        conn1 = Mock()
        conn1.read.side_effect = [ReplyError('MOVED 42 host2:12345')]
        conn2 = Mock()
        conn2.read.side_effect = ['success']
        self.connection_mock.side_effect = [conn1, conn2]

        self.client._cleanup_conns = Mock()

        id = self.client._map_id

        result = self.client.execute('GET', 'test', shard_key='test')
        self.assertEqual(result, 'success')
        conn1.write.assert_called_with('GET', 'test')
        conn2.write.assert_called_with('GET', 'test')
        self.assertTrue(self.client._cleanup_conns.called)
        self.clustermap_inst.update.assert_called_with(id)

    def test_execute_ReplyError_to_many_retries(self):
        self.client._get_slot_info = Mock()
        self.client._get_slot_info.side_effect = [
            'host1_12345',
            'host2_12345',
            'host3_12345',
            'host4_12345'
        ]
        conn1 = Mock()
        conn1.read.side_effect = [ReplyError('MOVED 42 host2:12345')]
        conn2 = Mock()
        conn2.read.side_effect = [ReplyError('MOVED 42 host2:12345')]
        conn3 = Mock()
        conn3.read.side_effect = [ReplyError('MOVED 42 host2:12345')]
        conn4 = Mock()
        conn4.read.side_effect = [ReplyError('MOVED 42 host2:12345')]
        self.connection_mock.side_effect = [conn1, conn2, conn3, conn4]

        self.client._cleanup_conns = Mock()

        self.assertRaises(PyRedisError, self.client.execute, 'GET', 'test', shard_key='test')

        conn1.write.assert_called_with('GET', 'test')
        conn2.write.assert_called_with('GET', 'test')
        conn3.write.assert_called_with('GET', 'test')
        self.assertFalse(conn4.write.called)

    def test_execute_PyRedisConnError(self):
        self.client._get_slot_info = Mock()
        self.client._get_slot_info.side_effect = ['host1_12345']
        conn1 = Mock()
        conn1.read.side_effect = [PyRedisConnError]
        self.connection_mock.side_effect = [conn1]

        self.assertRaises(PyRedisConnError, self.client.execute, 'GET', 'test', shard_key='test')
        self.assertTrue(conn1.close.called)
        self.assertNotIn(conn1, self.client._conns)
        self.clustermap_inst.update.assert_called_with(self.client._map_id)

    def test_execute_PyRedisConnReadTimeout(self):
        self.client._get_slot_info = Mock()
        self.client._get_slot_info.side_effect = ['host1_12345']
        conn1 = Mock()
        conn1.read.side_effect = [PyRedisConnReadTimeout]
        self.connection_mock.side_effect = [conn1]

        self.assertRaises(PyRedisConnReadTimeout, self.client.execute, 'GET', 'test', shard_key='test')
        self.assertTrue(conn1.close.called)
        self.assertNotIn(conn1, self.client._conns)
        self.clustermap_inst.update.assert_called_with(self.client._map_id)
