from unittest import TestCase
from unittest.mock import Mock, MagicMock, PropertyMock, call, patch

from pyredis.exceptions import *

import pyredis.connection
from pyredis.protocol import writer, Reader
import socket


class TestConnectionUnit(TestCase):
    def setUp(self):
        self.addCleanup(patch.stopall)

        socket_patcher = patch('pyredis.connection.socket', autospec=True)
        self.socket_mock = socket_patcher.start()
        self.socket_mock.socket.return_value = Mock()

        reader_patcher = patch('pyredis.connection.Reader', autospec=True)
        self.reader_mock = reader_patcher.start()

    def test___init___default_args_host(self):
        connection = pyredis.connection.Connection(host='127.0.0.1')
        self.assertEqual(connection._conn_timeout, 2)
        self.assertEqual(connection._read_timeout, 2)
        self.assertEqual(connection.host, '127.0.0.1')
        self.assertEqual(connection.port, 6379)
        self.assertEqual(connection._writer, pyredis.connection.writer)
        self.assertIsNone(connection.password)
        self.assertIsNone(connection._reader)
        self.assertIsNone(connection._encoding)
        self.assertFalse(connection._closed)

    def test___init___default_args_unix_sock(self):
        connection = pyredis.connection.Connection(unix_sock='/tmp/test.sock')
        self.assertEqual(connection._conn_timeout, 2)
        self.assertEqual(connection._read_timeout, 2)
        self.assertEqual(connection.unix_sock, '/tmp/test.sock')
        self.assertEqual(connection._writer, pyredis.connection.writer)
        self.assertIsNone(connection.password)
        self.assertIsNone(connection._reader)
        self.assertFalse(connection._closed)

    def test___init___custom_args(self):
        connection = pyredis.connection.Connection(
            host='127.0.0.4', port=1234, password='blubber',
            conn_timeout=10, read_timeout=11, encoding='utf-8'
        )
        self.assertEqual(connection.host, '127.0.0.4')
        self.assertEqual(connection.port, 1234)
        self.assertEqual(connection.password, 'blubber')
        self.assertEqual(connection._conn_timeout, 10)
        self.assertEqual(connection._read_timeout, 11)
        self.assertEqual(connection._writer, pyredis.connection.writer)
        self.assertEqual(connection._encoding, 'utf-8')
        self.assertIsNone(connection._reader)
        self.assertFalse(connection._closed)

    def test___init___no_host_or_unix_sock(self):
        self.assertRaises(PyRedisError, pyredis.connection.Connection)

    def test___init___both_host_and_unix_sock(self):
        self.assertRaises(
            PyRedisError,
            pyredis.connection.Connection,
            host='127.0.0.1',
            unix_sock='/tmp/test.sock'
        )

    def test__authenticate_ok(self):
        connection = pyredis.connection.Connection(host='127.0.0.1', password='testpass')
        connection.write = Mock()
        connection.read = Mock()
        connection.read.return_value = b'OK'
        connection._sock = Mock()
        connection._authenticate()
        connection.write.assert_called_with('AUTH', 'testpass')

    def test__authenticate_exception(self):
        connection = pyredis.connection.Connection(host='127.0.0.1', password='testpass')
        connection.write = Mock()
        connection.read = Mock()
        connection.read.side_effect = ReplyError
        connection._sock = Mock()
        self.assertRaises(ReplyError, connection._authenticate)
        connection.write.assert_called_with('AUTH', 'testpass')

    def test__connect_inet46_ipv4(self):
        connection = pyredis.connection.Connection(host='127.0.0.1')
        sock = connection._connect_inet46()
        self.socket_mock.socket.assert_called_with(
            self.socket_mock.AF_INET,
            self.socket_mock.SOCK_STREAM
        )
        sock.settimeout.assert_called_with(2)
        sock.connect.assert_called_with(('127.0.0.1', 6379))
        self.assertEqual(sock, self.socket_mock.socket())

    def test__connect_inet46_ipv6(self):
        sock_mock = Mock()
        self.socket_mock.socket.side_effect = [socket.gaierror, sock_mock]
        self.socket_mock.gaierror = socket.gaierror

        connection = pyredis.connection.Connection(host='::1')
        sock = connection._connect_inet46()

        self.socket_mock.socket.assert_has_calls([
            call(
                self.socket_mock.AF_INET,
                self.socket_mock.SOCK_STREAM
            ),
            call(
                self.socket_mock.AF_INET6,
                self.socket_mock.SOCK_STREAM
            )
        ])

        sock.settimeout.assert_called_with(2)
        sock.connect.assert_called_with(('::1', 6379))
        self.assertEqual(sock, sock_mock)

    def test__connect_inet46_no_ipv4_or_ipv6(self):
        self.socket_mock.socket.side_effect = [socket.gaierror, socket.gaierror]
        self.socket_mock.gaierror = socket.gaierror

        connection = pyredis.connection.Connection(host='blarg')
        self.assertRaises(PyRedisConnError, connection._connect_inet46)

    def test__connect_inet46_socket_timeout(self):
        sock_mock = Mock()
        sock_mock.connect.side_effect = socket.timeout

        self.socket_mock.socket.return_value = sock_mock
        self.socket_mock.gaierror = socket.gaierror
        self.socket_mock.timeout = socket.timeout

        connection = pyredis.connection.Connection(host='127.0.0.1')
        self.assertRaises(PyRedisConnError, connection._connect_inet46)

    def test__connect_inet46_OverflowError(self):
        sock_mock = Mock()
        sock_mock.connect.side_effect = OverflowError

        self.socket_mock.gaierror = socket.gaierror
        self.socket_mock.timeout = socket.timeout

        self.socket_mock.socket.return_value = sock_mock

        connection = pyredis.connection.Connection(host='127.0.0.1')
        self.assertRaises(PyRedisConnError, connection._connect_inet46)

    def test__connect_inet46_ConnectionRefusedError(self):
        sock_mock = Mock()
        sock_mock.connect.side_effect = ConnectionRefusedError

        self.socket_mock.gaierror = socket.gaierror
        self.socket_mock.timeout = socket.timeout

        self.socket_mock.socket.return_value = sock_mock

        connection = pyredis.connection.Connection(host='127.0.0.1')
        self.assertRaises(PyRedisConnError, connection._connect_inet46)

    def test__connect_inet46_ConnectionAbortedError(self):
        sock_mock = Mock()
        sock_mock.connect.side_effect = ConnectionAbortedError

        self.socket_mock.gaierror = socket.gaierror
        self.socket_mock.timeout = socket.timeout

        self.socket_mock.socket.return_value = sock_mock

        connection = pyredis.connection.Connection(host='127.0.0.1')
        self.assertRaises(PyRedisConnError, connection._connect_inet46)

    def test__connect_unix(self):
        connection = pyredis.connection.Connection(unix_sock='/tmp/test.sock')
        sock = connection._connect_unix()
        self.socket_mock.socket.assert_called_with(
            self.socket_mock.AF_UNIX,
            self.socket_mock.SOCK_STREAM
        )
        sock.settimeout.assert_called_with(2)
        sock.connect.assert_called_with('/tmp/test.sock')
        self.assertEqual(sock, self.socket_mock.socket())

    def test__connect_unix_ConnectionRefusedError(self):
        sock_mock = Mock()
        sock_mock.connect.side_effect = ConnectionRefusedError

        self.socket_mock.timeout = socket.timeout

        self.socket_mock.socket.return_value = sock_mock

        connection = pyredis.connection.Connection(unix_sock='/tmp/test.sock')

        self.assertRaises(PyRedisConnError, connection._connect_unix)

    def test__connect_unix_socket_timeout(self):
        sock_mock = Mock()
        sock_mock.connect.side_effect = socket.timeout

        self.socket_mock.timeout = socket.timeout

        self.socket_mock.socket.return_value = sock_mock

        connection = pyredis.connection.Connection(unix_sock='/tmp/test.sock')

        self.assertRaises(PyRedisConnError, connection._connect_unix)

    def test__connect_unix_FileNotFoundError(self):
        sock_mock = Mock()
        sock_mock.connect.side_effect = FileNotFoundError

        self.socket_mock.timeout = socket.timeout

        self.socket_mock.socket.return_value = sock_mock

        connection = pyredis.connection.Connection(unix_sock='/tmp/test.sock')

        self.assertRaises(PyRedisConnError, connection._connect_unix)

    def test__connect_ipv4(self):
        sock_mock = Mock()
        self.socket_mock.socket.return_value = sock_mock
        reader_mock = Mock()
        self.reader_mock.return_value = reader_mock

        connection = pyredis.connection.Connection(host='127.0.0.1')
        connection._authenticate = Mock()
        connection._setdb = Mock()
        connection._connect()

        sock_mock.settimeout.assert_called_with(2)
        self.assertEqual(connection._sock, self.socket_mock.socket())
        self.assertEqual(connection._reader, reader_mock)
        self.assertIsNone(connection._encoding)
        self.reader_mock.assert_called_with()

    def test__connect_ipv4_encoding_utf_8(self):
        sock_mock = Mock()
        self.socket_mock.socket.return_value = sock_mock
        reader_mock = Mock()
        self.reader_mock.return_value = reader_mock

        connection = pyredis.connection.Connection(host='127.0.0.1', encoding='utf-8')
        connection._authenticate = Mock()
        connection._setdb = Mock()
        connection._connect()

        sock_mock.settimeout.assert_called_with(2)
        self.assertEqual(connection._sock, self.socket_mock.socket())
        self.assertEqual(connection._encoding, 'utf-8')
        self.assertEqual(connection._reader, reader_mock)
        self.reader_mock.assert_called_with(encoding='utf-8')

    def test__connect_ipv6(self):
        sock_mock = Mock()
        self.socket_mock.socket.return_value = sock_mock
        reader_mock = Mock()
        self.reader_mock.return_value = reader_mock

        connection = pyredis.connection.Connection(host='::1')
        connection._authenticate = Mock()
        connection._setdb = Mock()
        connection._connect()

        sock_mock.settimeout.assert_called_with(2)

    def test__close(self):
        sock_mock = Mock()
        self.socket_mock.socket.return_value = sock_mock

        connection = pyredis.connection.Connection(unix_sock='/tmp/test.sock')
        connection._authenticate = Mock()
        connection._setdb = Mock()
        connection._connect()
        connection.close()

        sock_mock.close.assert_called_with()
        self.assertIsNone(connection._sock)
        self.assertIsNone(connection._reader)
        self.assertTrue(connection._closed)

    def test__setdb(self):
        connection = pyredis.connection.Connection(host='localhost')
        connection.read = Mock()
        connection.read.return_value = b'OK'
        connection.write = Mock()
        connection._sock = Mock()
        connection._setdb()
        connection.write.assert_called_with('SELECT', 0)
        connection.read.assert_called_with()

    def test__setdb_invalid_db(self):
        connection = pyredis.connection.Connection(host='localhost', database=23234)
        connection.read = Mock()
        connection.read.side_effect = ReplyError
        connection.write = Mock()
        connection._sock = Mock()
        self.assertRaises(ReplyError, connection._setdb)
        connection.write.assert_called_with('SELECT', 23234)
        connection.read.assert_called_with()

    def test_closed_false(self):
        connection = pyredis.connection.Connection(unix_sock='/tmp/test.sock')
        self.assertFalse(connection.closed)

    def test_closed_true(self):
        connection = pyredis.connection.Connection(unix_sock='/tmp/test.sock')
        connection._closed = True
        self.assertTrue(connection.closed)

    def test_write_one_chunk(self):
        cmd = 'ECHO'
        payload = "x" * 512
        msg = writer(cmd, payload)
        length = 534

        sock_mock = Mock()

        sock_mock.send.side_effect = [length]
        self.socket_mock.socket.return_value = sock_mock

        reader_mock = Mock()
        self.reader_mock.return_value = reader_mock

        connection = pyredis.connection.Connection(host='127.0.0.1', encoding='utf-8')
        connection._authenticate = Mock()
        connection._setdb = Mock()
        connection.write(cmd, payload)

        self.assertEqual(sock_mock.send.call_args_list, [call(msg)])

    def test_write_two_chunks(self):
        cmd = 'ECHO'
        payload = "x" * 512
        msg = writer(cmd, payload)

        sock_mock = Mock()

        sock_mock.send.side_effect = [500, 34]
        self.socket_mock.socket.return_value = sock_mock

        reader_mock = Mock()
        self.reader_mock.return_value = reader_mock

        connection = pyredis.connection.Connection(host='127.0.0.1', encoding='utf-8')
        connection._authenticate = Mock()
        connection._setdb = Mock()
        connection.write(cmd, payload)

        self.assertEqual(sock_mock.send.call_args_list, [call(msg), call(msg[500:])])

    def test_write_exception_brokenpipeerror(self):
        cmd = 'ECHO'
        payload = "x" * 512

        sock_mock = Mock()

        sock_mock.send.side_effect = [BrokenPipeError]
        self.socket_mock.socket.return_value = sock_mock

        reader_mock = Mock()
        self.reader_mock.return_value = reader_mock

        connection = pyredis.connection.Connection(host='127.0.0.1', encoding='utf-8')
        connection._authenticate = Mock()
        connection._setdb = Mock()
        connection._connect()
        self.assertRaises(PyRedisConnError, connection.write, cmd, payload)

    def test_read_one_chunk_one_message(self):
        raw_answer = b'$10\r\nXXXXXXXXXX\r\n'
        answer = 'XXXXXXXXXX'

        sock_mock = Mock()
        sock_mock.recv.side_effect = [raw_answer]
        self.socket_mock.socket.return_value = sock_mock

        reader_mock = Mock()
        self.reader_mock.return_value = reader_mock

        connection = pyredis.connection.Connection(host='127.0.0.1', encoding='utf-8')
        connection._authenticate = Mock()
        connection._setdb = Mock()
        pyredis.connection.Reader = Reader
        connection._connect()
        result = connection.read()
        self.assertEqual(result, answer)

    def test_read_two_chunks_one_message(self):
        raw_answer1 = b'$10\r\nXXX'
        raw_answer2 = b'XXXXXXX\r\n'
        answer = 'XXXXXXXXXX'

        sock_mock = Mock()
        sock_mock.recv.side_effect = [raw_answer1, raw_answer2]
        self.socket_mock.socket.return_value = sock_mock

        reader_mock = Mock()
        self.reader_mock.return_value = reader_mock

        connection = pyredis.connection.Connection(host='127.0.0.1', encoding='utf-8')
        connection._authenticate = Mock()
        connection._setdb = Mock()
        pyredis.connection.Reader = Reader
        connection._connect()
        result = connection.read()
        self.assertEqual(result, answer)

    def test_read_one_chunk_two_messages(self):
        raw_answer = b'$10\r\nXXXXXXXXXX\r\n$10\r\nYYYYYYYYYY\r\n'
        answer = 'XXXXXXXXXX'

        sock_mock = Mock()
        sock_mock.recv.side_effect = [raw_answer]
        self.socket_mock.socket.return_value = sock_mock

        reader_mock = Mock()
        self.reader_mock.return_value = reader_mock

        connection = pyredis.connection.Connection(host='127.0.0.1', encoding='utf-8')
        connection._authenticate = Mock()
        connection._setdb = Mock()
        pyredis.connection.Reader = Reader
        connection._connect()
        result = connection.read()
        self.assertEqual(result, answer)

    def test_read_message_ready_from_previous_chunck(self):
        raw_answer = b'$10\r\nXXXXXXXXXX\r\n$10\r\nYYYYYYYYYY\r\n'
        answer1 = 'XXXXXXXXXX'
        answer2 = 'YYYYYYYYYY'

        sock_mock = Mock()
        sock_mock.recv.side_effect = [raw_answer]
        self.socket_mock.socket.return_value = sock_mock

        reader_mock = Mock()
        self.reader_mock.return_value = reader_mock

        connection = pyredis.connection.Connection(host='127.0.0.1', encoding='utf-8')
        connection._authenticate = Mock()
        connection._setdb = Mock()
        pyredis.connection.Reader = Reader
        connection._connect()
        result1 = connection.read()
        result2 = connection.read()
        self.assertEqual(result1, answer1)
        self.assertEqual(result2, answer2)
        self.assertEqual(sock_mock.recv.call_args_list, [call(1500)])

    def test_read_exception_not_connected(self):
        connection = pyredis.connection.Connection(host='127.0.0.1', encoding='utf-8')
        self.assertRaises(PyRedisConnError, connection.read)

    def test_read_exception_socket_timeout(self):
        sock_mock = Mock()
        sock_mock.recv.side_effect = [socket.timeout]
        self.socket_mock.socket.return_value = sock_mock
        self.socket_mock.timeout = socket.timeout

        reader_mock = Mock()
        self.reader_mock.return_value = reader_mock

        connection = pyredis.connection.Connection(host='127.0.0.1', encoding='utf-8')
        connection._authenticate = Mock()
        connection._setdb = Mock()
        pyredis.connection.Reader = Reader
        connection._connect()
        self.assertRaises(PyRedisConnReadTimeout, connection.read)
        self.assertTrue(connection.closed)

    def test_read_exception_socket_timeout_close_on_timeout_false(self):
        sock_mock = Mock()
        sock_mock.recv.side_effect = [socket.timeout]
        self.socket_mock.socket.return_value = sock_mock
        self.socket_mock.timeout = socket.timeout

        reader_mock = Mock()
        self.reader_mock.return_value = reader_mock

        connection = pyredis.connection.Connection(host='127.0.0.1', encoding='utf-8')
        connection._authenticate = Mock()
        connection._setdb = Mock()
        pyredis.connection.Reader = Reader
        connection._connect()
        self.assertRaises(PyRedisConnReadTimeout, connection.read, close_on_timeout=False)
        self.assertFalse(connection.closed)

    def test_read_exception_connection_lost(self):
        sock_mock = Mock()
        sock_mock.recv.side_effect = ['']
        self.socket_mock.socket.return_value = sock_mock

        reader_mock = Mock()
        self.reader_mock.return_value = reader_mock

        connection = pyredis.connection.Connection(host='127.0.0.1', encoding='utf-8')
        connection._authenticate = Mock()
        connection._setdb = Mock()
        pyredis.connection.Reader = Reader
        connection._connect()
        self.assertRaises(PyRedisConnClosed, connection.read)
        self.assertTrue(connection.closed)

    def test_read_exception_result_raise(self):
        connection = pyredis.connection.Connection(host='127.0.0.1', encoding='utf-8')
        connection._sock = True

        reader_mock = Mock()
        reader_mock.gets.return_value = ReplyError('blub')
        connection._reader = reader_mock
        self.assertRaises(ReplyError, connection.read)

    def test_read_exception_result_no_raise(self):
        connection = pyredis.connection.Connection(host='127.0.0.1', encoding='utf-8')
        connection._sock = True

        reader_mock = Mock()
        reader_mock.gets.return_value = ReplyError('blub')
        connection._reader = reader_mock
        connection.read(raise_on_result_err=False)
