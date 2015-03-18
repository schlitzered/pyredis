__author__ = 'schlitzer'

from unittest import TestCase
from unittest.mock import Mock, MagicMock, PropertyMock, call, patch

from collections import deque

import pyredis.client
from pyredis.exceptions import *


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

    def test_bulk_stop(self):
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


class TestPubSubClientUnit(TestCase):
    def setUp(self):
        self.addCleanup(patch.stopall)

        connection_patcher = patch('pyredis.client.Connection', autospec=True)
        self.connection_mock = connection_patcher.start()

    def test_get(self):
        conn_mock = Mock()
        conn_mock.read.return_value = 'something'
        self.connection_mock.return_value = conn_mock

        client = pyredis.client.PubSubClient(host='localhost')
        self.assertEqual(client._conn, conn_mock)
        self.connection_mock.assert_called_with(
            host='localhost')
        result = client.get()
        conn_mock.read.assert_called_with(close_on_timeout=False)
        self.assertEqual(result, 'something')


class TestSentinelClientUnit(TestCase):
    def setUp(self):
        self.addCleanup(patch.stopall)

        connection_patcher = patch('pyredis.client.Connection', autospec=True)
        self.connection_mock = connection_patcher.start()

        dict_from_list_patcher = patch('pyredis.client.dict_from_list', autospec=True)
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
        client = pyredis.client.SentinelClient(sentinels=sentinels)
        client.execute = Mock()

        self.assertTrue(client._sentinel_connect(sentinel=('host1', 12345)))
        self.connection_mock.assert_called_with(
            host='host1', port=12345, conn_timeout=0.1, sentinel=True)
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
            host='host1', port=12345, conn_timeout=0.1, sentinel=True)
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
        self.dict_from_list_mock.side_effect = (dict_expected1, dict_expected2)
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
        self.dict_from_list_mock.side_effect = (dict_expected1, dict_expected2)
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
        client.close.assert_called_wit()
        self.assertEqual(client.sentinels, expected)
