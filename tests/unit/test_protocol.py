from unittest import TestCase
import pyredis.protocol as hiredis
from pyredis.protocol import writer, to_bytes
import sys

# The class ReaderTest is more or less copied from the hiredis python package.
# The Licence Terms of hiredis (BSD) appeal to the ReaderTest class!


class ReaderTest(TestCase):
    def setUp(self):
        self.reader = hiredis.Reader()

    def reply(self):
        return self.reader.gets()

    def test_nothing(self):
        self.assertEqual(False, self.reply())

    def test_error_when_feeding_non_string(self):
        self.assertRaises(TypeError, self.reader.feed, 1)

    def test_protocol_error(self):
        self.reader.feed(b'x')
        self.assertRaises(hiredis.ProtocolError, self.reply)

    def test_protocol_error_with_custom_class(self):
        self.reader = hiredis.Reader(protocolError=RuntimeError)
        self.reader.feed(b'x')
        self.assertRaises(RuntimeError, self.reply)

    def test_protocol_error_with_custom_callable(self):
        class CustomException(Exception):
            pass

        self.reader = hiredis.Reader(protocolError=lambda e: CustomException(e))
        self.reader.feed(b'x')
        self.assertRaises(CustomException, self.reply)

    def test_fail_with_wrong_protocol_error_class(self):
        self.assertRaises(TypeError, hiredis.Reader, protocolError='wrong')

    def test_error_string(self):
        self.reader.feed(b'-error\r\n')
        error = self.reply()

        self.assertEqual(hiredis.ReplyError, type(error))
        self.assertEqual(('error',), error.args)

    def test_error_string_partial(self):
        self.reader.feed(b'-err')
        self.assertFalse(self.reply())
        self.reader.feed(b'or\r\n')
        error = self.reply()

        self.assertEqual(hiredis.ReplyError, type(error))
        self.assertEqual(('error',), error.args)

    def test_error_string_partial_footer(self):
        self.reader.feed(b'-error')
        self.assertFalse(self.reply())
        self.reader.feed(b'\r')
        self.assertFalse(self.reply())
        self.reader.feed(b'\n')
        error = self.reply()

        self.assertEqual(hiredis.ReplyError, type(error))
        self.assertEqual(('error',), error.args)

    def test_error_string_with_custom_class(self):
        self.reader = hiredis.Reader(replyError=RuntimeError)
        self.reader.feed(b'-error\r\n')
        error = self.reply()

        self.assertEqual(RuntimeError, type(error))
        self.assertEqual(('error',), error.args)

    def test_error_string_with_custom_callable(self):
        class CustomException(Exception):
            pass

        self.reader = hiredis.Reader(replyError=lambda e: CustomException(e))
        self.reader.feed(b'-error\r\n')
        error = self.reply()

        self.assertEqual(CustomException, type(error))
        self.assertEqual(('error',), error.args)

    def test_fail_with_wrong_reply_error_class(self):
        self.assertRaises(TypeError, hiredis.Reader, replyError='wrong')

    def test_errors_in_nested_multi_bulk(self):
        self.reader.feed(b'*2\r\n-err0\r\n-err1\r\n')

        for r, error in zip(('err0', 'err1'), self.reply()):
            self.assertEqual(hiredis.ReplyError, type(error))
            self.assertEqual((r,), error.args)

    def test_integer(self):
        value = 2 ** 63 - 1  # Largest 64-bit signed integer
        self.reader.feed((':{0}\r\n'.format(value)).encode('ascii'))
        self.assertEqual(value, self.reply())

    def test_integer_partial_int(self):
        value = 2 ** 63 - 1  # Largest 64-bit signed integer
        strvalue = str(value).encode('ascii')
        part1, part2 = strvalue[:6], strvalue[6:]
        self.reader.feed(b':')
        self.reader.feed(part1)
        self.assertFalse(self.reply())
        self.reader.feed(part2)
        self.reader.feed(b'\r\n')
        self.assertEqual(value, self.reply())

    def test_integer_partial_footer(self):
        value = 2 ** 63 - 1  # Largest 64-bit signed integer
        self.reader.feed((':{0}'.format(value)).encode('ascii'))
        self.assertFalse(self.reply())
        self.reader.feed(b'\r')
        self.assertFalse(self.reply())
        self.reader.feed(b'\n')
        self.assertEqual(value, self.reply())

    def test_status_string(self):
        self.reader.feed(b'+ok\r\n')
        self.assertEqual(b'ok', self.reply())

    def test_status_string_partial(self):
        self.reader.feed(b'+ok')
        self.assertFalse(self.reply())
        self.reader.feed(b'ok\r\n')
        self.assertEqual(b'okok', self.reply())

    def test_status_string_partial_footer(self):
        self.reader.feed(b'+ok')
        self.assertFalse(self.reply())
        self.reader.feed(b'\r')
        self.assertFalse(self.reply())
        self.reader.feed(b'\n')
        self.assertEqual(b'ok', self.reply())

    def test_empty_bulk_string(self):
        self.reader.feed(b'$0\r\n\r\n')
        self.assertEqual(b'', self.reply())

    def test_NULL_bulk_string(self):
        self.reader.feed(b'$-1\r\n')
        self.assertEqual(None, self.reply())

    def test_bulk_string(self):
        self.reader.feed(b'$5\r\nhello\r\n')
        self.assertEqual(b'hello', self.reply())

    def test_bulk_string_partial(self):
        self.reader.feed(b'$5\r\nhel')
        self.assertFalse(self.reply())
        self.assertFalse(self.reply())
        self.reader.feed(b'lo\r\n')
        self.assertEqual(b'hello', self.reply())

    def test_bulk_string_partial_footer(self):
        self.reader.feed(b'$5\r\nhello')
        self.assertFalse(self.reply())
        self.reader.feed(b'\r')
        self.assertFalse(self.reply())
        self.reader.feed(b'\n')
        self.assertEqual(b'hello', self.reply())

    def test_bulk_string_without_encoding(self):
        snowman = b'\xe2\x98\x83'
        self.reader.feed(b'$3\r\n' + snowman + b'\r\n')
        self.assertEqual(snowman, self.reply())

    def test_bulk_string_with_encoding(self):
        snowman = b'\xe2\x98\x83'
        self.reader = hiredis.Reader(encoding='utf-8')
        self.reader.feed(b'$3\r\n' + snowman + b'\r\n')
        self.assertEqual(snowman.decode('utf-8'), self.reply())

    def test_bulk_string_with_other_encoding(self):
        snowman = b'\xe2\x98\x83'
        self.reader = hiredis.Reader(encoding='utf-32')
        self.reader.feed(b'$3\r\n' + snowman + b'\r\n')
        self.assertEqual(snowman, self.reply())

    def test_bulk_string_with_invalid_encoding(self):
        self.reader = hiredis.Reader(encoding='unknown')
        self.reader.feed(b'$5\r\nhello\r\n')
        self.assertRaises(LookupError, self.reply)

    def test_null_multi_bulk(self):
        self.reader.feed(b'*-1\r\n')
        self.assertEqual(None, self.reply())

    def test_empty_multi_bulk(self):
        self.reader.feed(b'*0\r\n')
        self.assertEqual([], self.reply())

    def test_multi_bulk(self):
        self.reader.feed(b'*2\r\n$5\r\nhello\r\n$5\r\nworld\r\n')
        self.assertEqual([b'hello', b'world'], self.reply())

    def test_multi_bulk_with_partial_reply(self):
        self.reader.feed(b'*2\r\n$5\r\nhello\r\n')
        self.assertEqual(False, self.reply())
        self.reader.feed(b':1\r\n')
        self.assertEqual([b'hello', 1], self.reply())

    def test_nested_multi_bulk(self):
        self.reader.feed(b'*2\r\n*2\r\n$5\r\nhello\r\n$5\r\nworld\r\n$1\r\n!\r\n')
        self.assertEqual([[b'hello', b'world'], b'!'], self.reply())

    def test_nested_multi_bulk_partial(self):
        self.reader.feed(b'*2\r\n*2\r\n$5\r\nhello\r')
        self.assertEqual(False, self.reply())
        self.reader.feed(b'\n$5\r\nworld\r\n$1\r\n!\r\n')
        self.assertEqual([[b'hello', b'world'], b'!'], self.reply())

    def test_nested_multi_bulk_depth(self):
        self.reader.feed(b'*1\r\n*1\r\n*1\r\n*1\r\n$1\r\n!\r\n')
        self.assertEqual([[[[b'!']]]], self.reply())

    def test_subclassable(self):
        class TestReader(hiredis.Reader):
            def __init__(self, *args, **kwargs):
                super(TestReader, self).__init__(*args, **kwargs)

        reader = TestReader()
        reader.feed(b'+ok\r\n')
        self.assertEqual(b'ok', reader.gets())

    def test_invalid_offset(self):
        data = b'+ok\r\n'
        self.assertRaises(ValueError, self.reader.feed, data, 6)

    def test_invalid_length(self):
        data = b'+ok\r\n'
        self.assertRaises(ValueError, self.reader.feed, data, 0, 6)

    def test_ok_offset(self):
        data = b'blah+ok\r\n'
        self.reader.feed(data, 4)
        self.assertEqual(b'ok', self.reply())

    def test_ok_length(self):
        data = b'blah+ok\r\n'
        self.reader.feed(data, 4, len(data) - 4)
        self.assertEqual(b'ok', self.reply())

    def test_feed_bytearray(self):
        if sys.hexversion >= 0x02060000:
            self.reader.feed(bytearray(b'+ok\r\n'))
            self.assertEqual(b'ok', self.reply())


class TestWriter(TestCase):
    def test_encode_0_args(self):
        expected = b'*0\r\n'
        self.assertEqual(
            writer(),
            expected)

    def test_encode_1_args(self):
        expected = b'*1\r\n$4\r\nPING\r\n'
        self.assertEqual(
            writer('PING'),
            expected)

    def test_encode_2_args(self):
        expected = b'*2\r\n$4\r\nECHO\r\n$14\r\nTest!!!!111elf\r\n'
        self.assertEqual(
            writer('ECHO', 'Test!!!!111elf'),
            expected)

    def test_encode_3_args(self):
        expected = b'*3\r\n$3\r\nSET\r\n$8\r\nKey/Name\r\n$19\r\nSomeValue_?#!\xc3\x84\xc3\x9c\xc3\x96\r\n'
        self.assertEqual(
            writer('SET', 'Key/Name', 'SomeValue_?#!ÄÜÖ'),
            expected)


class TestToBytes(TestCase):
    def test_int(self):
        expected = b'512'
        result = to_bytes(512)
        self.assertEqual(result, expected)

    def test_float(self):
        expected = b'0.815'
        result = to_bytes(0.815)
        self.assertEqual(result, expected)

    def test_str(self):
        expected = b'\xc3\xbc\xc3\x9f_blarg'
        result = to_bytes('üß_blarg')
        self.assertEqual(result, expected)

    def test_bytes(self):
        expected = b'0815'
        result = to_bytes(b'0815')
        self.assertEqual(result, expected)

    def test_ValueError(self):
        self.assertRaises(ValueError, to_bytes, object())
