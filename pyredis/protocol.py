import sys
from io import BytesIO
from pyredis.exceptions import ProtocolError, ReplyError

SYM_CRLF = b'\r\n'
SYM_EMPTY = b''

TYPE_SIMPLE = b'+'
TYPE_ERROR = b'-'
TYPE_INT = b':'
TYPE_BULK = b'$'
TYPE_ARRAY = b'*'

__all__ = [
    'Reader',
    'writer'
]


def is_exception(inst, classinfo):
    try:
        if issubclass(inst, classinfo):
            return True
        else:
            raise TypeError()
    except TypeError:
        if isinstance(inst('test'), classinfo):
            return True
        else:
            raise TypeError('{0} is not a subclass of {1}'.format(inst, classinfo))


class ReplyParser(object):
    def __init__(self, encoding, source, protocol_error=ProtocolError, reply_error=ReplyError):
        self._len = 0
        self._nested_parser = None
        self._encoding = encoding
        self._protocol_error = protocol_error
        self._reply_error = reply_error
        self._todo = self.header
        self._source = source
        self.complete = False
        self.result = b''

    def decode(self, data):
        if self._encoding:
            try:
                return data.decode(self._encoding)
            except UnicodeDecodeError:
                return data
        else:
            return data

    def header(self):
        byte = self._source.read(1)
        if byte == TYPE_ARRAY:
            return self.parse_array
        elif byte == TYPE_BULK:
            return self.parse_bulk
        elif byte == TYPE_SIMPLE:
            return self.parse_str
        elif byte == TYPE_INT:
            return self.parse_int
        elif byte == TYPE_ERROR:
            return self.parse_error
        elif byte == SYM_EMPTY:
            return None
        else:
            raise self._protocol_error('Protocol error, got {0} as reply type byte'.format(byte))

    def parse(self):
        while not self.complete:
            result = self._todo()
            if not result:
                return
            else:
                self._todo = result
        return True

    def parse_array(self):
        if not self._len:
            array_len = self.readline()
            if array_len:
                self._len = int(array_len)
                if int(array_len) >= 0:
                    self.result = []
                else:
                    self.result = None
            else:
                return
        try:
            while len(self.result) < self._len:
                if not self._nested_parser:
                    self._nested_parser = ReplyParser(
                        self._encoding,
                        self._source,
                        self._protocol_error,
                        self._reply_error
                    )
                result = self._nested_parser.parse()
                if result:
                    self.result.append(self._nested_parser.result)
                    self._nested_parser.reset()
                else:
                    return
        except TypeError:
            pass
        self.complete = True
        return True

    def parse_bulk(self):
        if not self._len:
            bulk_len = self.readline()
            if bulk_len == b'-1':
                self.complete = True
                self.result = None
                return True
            elif bulk_len:
                self._len = int(bulk_len) + 2
            else:
                return
        self.result += self._source.read(self._len - len(self.result))
        if len(self.result) == self._len:
            self.complete = True
            self.result = self.decode(self.result.rstrip(SYM_CRLF))
            return True

    def parse_error(self):
        result = self.readline()
        if result:
            self.complete = True
            self.result = self._reply_error(result.decode(sys.getdefaultencoding()))
            return True

    def parse_int(self):
        result = self.readline()
        if result:
            self.complete = True
            self.result = int(result)
            return True

    def parse_str(self):
        result = self.readline()
        if result:
            self.complete = True
            self.result = result
            return True

    def readline(self):
        self.result += self._source.readline()
        if self.result.endswith(SYM_CRLF):
            result = self.result.rstrip(SYM_CRLF)
            self.result = b''
            return result

    def reset(self):
        self._len = None
        self._todo = self.header
        self._nested_parser = None
        self.complete = False
        self.result = b''


class Reader(object):
    def __init__(self, encoding=None, protocolError=ProtocolError, replyError=ReplyError):
        self._buffer = BytesIO()
        self._buffer_pos = 0
        self._encoding = encoding
        if is_exception(protocolError, Exception):
            self._protocol_error = protocolError
        if is_exception(replyError, Exception):
            self._reply_error = replyError
        self._replyparser = ReplyParser(
            self._encoding,
            self._buffer,
            self._protocol_error,
            self._reply_error
        )

    def _truncate(self):
        remain = BytesIO()
        self._buffer.seek(self._buffer_pos)
        remain.write(self._buffer.read())
        self._buffer = remain
        self._replyparser._source = self._buffer
        self._buffer_pos = 0
        self._buffer.seek(0)

    def feed(self, data, offset=None, length=None):
        if offset and length:
            if (offset + length > len(data)) or \
                    (offset or length) < 0:
                raise ValueError('offset+length bigger then available date')
            data = data[offset:][:length]
        elif offset:
            if (offset > len(data)) or (offset < 0):
                raise ValueError('offset bigger then available data')
            data = data[offset:]
        elif length:
            if (length > len(data)) or (length < 0):
                raise ValueError('length bigger then available data')
            data = data[:length]
        self._buffer.seek(0, 2)
        self._buffer.write(data)

    def gets(self):
        self._buffer.seek(self._buffer_pos)
        result = self._replyparser.parse()
        self._buffer_pos = self._buffer.tell()
        if result:
            result = self._replyparser.result
            self._truncate()
            self._replyparser.reset()
            return result
        return False


def to_bytes(value):
    if isinstance(value, str):
        return value.encode()
    elif isinstance(value, (int, float)):
        return str(value).encode()
    elif isinstance(value, bytes):
        return value
    else:
        raise ValueError('Unsupported value, has to be a instance of bytes, str, int or float')


def writer(*args):
    buf = list()

    buf.append(TYPE_ARRAY)
    buf.append(to_bytes(len(args)))
    buf.append(SYM_CRLF)

    for member in args:
        member = to_bytes(member)

        buf.append(TYPE_BULK)
        buf.append(to_bytes(len(member)))
        buf.append(SYM_CRLF)

        buf.append(member)
        buf.append(SYM_CRLF)

    return b''.join(buf)
