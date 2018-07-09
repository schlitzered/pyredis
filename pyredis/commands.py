__author__ = 'schlitzer'

__all__ = [
    'Connection',
    'Hash',
    'HyperLogLog',
    'Key',
    'List',
    'Publish',
    'Scripting',
    'Set',
    'SSet',
    'String',
    'Subscribe',
    'Transaction'
]


class BaseCommand(object):
    def __init__(self):
        self._cluster = False

    def execute(self, *args, **kwargs):
        raise NotImplemented


class Connection(BaseCommand):
    def __init__(self):
        super().__init__()

    def echo(self, *args, shard_key=None, sock=None):
        """ Execute ECHO Command, consult Redis documentation for details.

        :param shard_key: (optional)
            Should be set to the key name you try to work with.
            Can not be used if sock is set.

            Only used if used with a Cluster Client
        :type shard_key: string

        :param sock: (optional)
            The string representation of a socket, the command should be executed against.
            For example: "testhost_6379"
            Can not be used if shard_key is set.

            Only used if used with a Cluster Client
        :type sock: string

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'ECHO', *args, shard_key=shard_key, sock=sock)
        return self.execute(b'ECHO', *args)

    def ping(self, shard_key=None, sock=None):
        """ Execute PING Command, consult Redis documentation for details.

        :param shard_key: (optional)
            Should be set to the key name you try to work with.
            Can not be used if sock is set.

            Only used if used with a Cluster Client
        :type shard_key: string

        :param sock: (optional)
            The string representation of a socket, the command should be executed against.
            For example: "testhost_6379"
            Can not be used if shard_key is set.

            Only used if used with a Cluster Client
        :type sock: string

        :return: result,exception
        """
        if self._cluster:
            return self.execute(b'PING', shard_key=shard_key, sock=sock)
        return self.execute(b'PING')


class Geo(BaseCommand):
    def __init__(self):
        super().__init__()

    def geoadd(self, *args):
        """ Execute GEOADD Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'GEOADD', *args, shard_key=args[0])
        return self.execute(b'GEOADD', *args)

    def geodist(self, *args):
        """ Execute GEODIST Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'GEODIST', *args, shard_key=args[0])
        return self.execute(b'GEODIST', *args)

    def geohash(self, *args):
        """ Execute GEOHASH Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'GEOHASH', *args, shard_key=args[0])
        return self.execute(b'GEOHASH', *args)

    def georadius(self, *args):
        """ Execute GEORADIUS Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'GEORADIUS', *args, shard_key=args[0])
        return self.execute(b'GEORADIUS', *args)

    def geopos(self, *args):
        """ Execute GEOPOS Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'GEOPOS', *args, shard_key=args[0])
        return self.execute(b'GEOPOS', *args)

    def georadiusbymember(self, *args):
        """ Execute GEORADIUSBYMEMBER Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'GEORADIUSBYMEMBER', *args, shard_key=args[0])
        return self.execute(b'GEORADIUSBYMEMBER', *args)


class Key(BaseCommand):
    def __init__(self):
        super().__init__()

    def delete(self, *args):
        """ Execute DEL Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'DEL', *args, shard_key=args[0])
        return self.execute(b'DEL', *args)

    def dump(self, *args):
        """ Execute DUMP Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'DUMP', *args, shard_key=args[0])
        return self.execute(b'DUMP', *args)

    def exists(self, *args):
        """ Execute EXISTS Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'EXISTS', *args, shard_key=args[0])
        return self.execute(b'EXISTS', *args)

    def expire(self, *args):
        """ Execute EXPIRE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'EXPIRE', *args, shard_key=args[0])
        return self.execute(b'EXPIRE', *args)

    def expireat(self, *args):
        """ Execute EXPIREAT Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'EXPIREAT')
        return self.execute(b'EXPIREAT', *args)

    def keys(self, *args, shard_key=None, sock=None):
        """ Execute KEYS Command, consult Redis documentation for details.

        :param shard_key: (optional)
            Should be set to the key name you try to work with.
            Can not be used if sock is set.

            Only used if used with a Cluster Client
        :type shard_key: string

        :param sock: (optional)
            The string representation of a socket, the command should be executed against.
            For example: "testhost_6379"
            Can not be used if shard_key is set.

            Only used if used with a Cluster Client
        :type sock: string

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'KEYS', *args, shard_key=shard_key, sock=sock)
        return self.execute(b'KEYS', *args)

    def migrate(self, *args):
        """ Execute MIGRATE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            raise NotImplemented
        return self.execute(b'MIGRATE', *args)

    def move(self, *args):
        """ Execute MOVE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'MOVE', *args, shard_key=args[0])
        return self.execute(b'MOVE', *args)

    def object(self, *args, shard_key=None, sock=None):
        """ Execute OBJECT Command, consult Redis documentation for details.

        :param shard_key: (optional)
            Should be set to the key name you try to work with.
            Can not be used if sock is set.

            Only used if used with a Cluster Client
        :type shard_key: string

        :param sock: (optional)
            The string representation of a socket, the command should be executed against.
            For example: "testhost_6379"
            Can not be used if shard_key is set.

            Only used if used with a Cluster Client
        :type sock: string

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'DEL', *args, shard_key=shard_key, sock=sock)
        return self.execute(b'OBJECT', *args)

    def persist(self, *args):
        """ Execute PERSIST Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'PERSIST', *args, shard_key=args[0])
        return self.execute(b'PERSIST', *args)

    def pexpire(self, *args):
        """ Execute PEXPIRE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'PEXPIRE', *args, shard_key=args[0])
        return self.execute(b'PEXPIRE', *args)

    def pexpireat(self, *args):
        """ Execute PEXPIREAT Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'PEXPIREAT', *args, shard_key=args[0])
        return self.execute(b'PEXPIREAT', *args)

    def pttl(self, *args):
        """ Execute PTTL Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'PTTL', *args, shard_key=args[0])
        return self.execute(b'PTTL', *args)

    def randomkey(self, *args, shard_key=None, sock=None):
        """ Execute RANDOMKEY Command, consult Redis documentation for details.

        :param shard_key: (optional)
            Should be set to the key name you try to work with.
            Can not be used if sock is set.

            Only used if used with a Cluster Client
        :type shard_key: string

        :param sock: (optional)
            The string representation of a socket, the command should be executed against.
            For example: "testhost_6379"
            Can not be used if shard_key is set.

            Only used if used with a Cluster Client
        :type sock: string

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'RANDOMKEY', *args, shard_key=shard_key, sock=sock)
        return self.execute(b'RANDOMKEY', *args)

    def rename(self, *args):
        """ Execute RENAME Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'RENAME', *args, shard_key=args[0])
        return self.execute(b'RENAME', *args)

    def renamenx(self, *args):
        """ Execute RENAMENX Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'RENAMENX', *args, shard_key=args[0])
        return self.execute(b'RENAMENX', *args)

    def restore(self, *args):
        """ Execute RESTORE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'RESTORE', *args, shard_key=args[0])
        return self.execute(b'RESTORE', *args)

    def scan(self, *args, shard_key=None, sock=None):
        """ Execute SCAN Command, consult Redis documentation for details.

        :param shard_key: (optional)
            Should be set to the key name you try to work with.
            Can not be used if sock is set.

            Only used if used with a Cluster Client
        :type shard_key: string

        :param sock: (optional)
            The string representation of a socket, the command should be executed against.
            For example: "testhost_6379"
            Can not be used if shard_key is set.

            Only used if used with a Cluster Client
        :type sock: string

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'SCAN', *args, shard_key=shard_key, sock=sock)
        return self.execute(b'SCAN', *args)

    def sort(self, *args):
        """ Execute SORT Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'SORT', *args, shard_key=args[0])
        return self.execute(b'SORT', *args)

    def ttl(self, *args):
        """ Execute TTL Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'TTL', *args, shard_key=args[0])
        return self.execute(b'TTL', *args)

    def type(self, *args):
        """ Execute TYPE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'TYPE', *args, shard_key=args[0])
        return self.execute(b'TYPE', *args)

    def wait(self, *args):
        """ Execute WAIT Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'WAIT', *args, shard_key=args[0])
        return self.execute(b'WAIT', *args)


class String(BaseCommand):
    def __init__(self):
        super().__init__()

    def append(self, *args):
        """ Execute APPEND Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'APPEND', *args, shard_key=args[0])
        return self.execute(b'APPEND', *args)

    def bitcount(self, *args):
        """ Execute BITCOUNT Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'BITCOUNT', *args, shard_key=args[0])
        return self.execute(b'BITCOUNT', *args)

    def bitfield(self, *args):
        """ Execute BITFIELD Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'BITFIELD', *args, shard_key=args[0])
        return self.execute(b'BITFIELD', *args)

    def bitop(self, *args):
        """ Execute BITOP Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'BITOP', *args, shard_key=args[1])
        return self.execute(b'BITOP', *args)

    def bitpos(self, *args):
        """ Execute BITPOS Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'BITPOS', *args, shard_key=args[0])
        return self.execute(b'BITPOS', *args)

    def decr(self, *args):
        """ Execute DECR Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'DECR', *args, shard_key=args[0])
        return self.execute(b'DECR', *args)

    def decrby(self, *args):
        """ Execute DECRBY Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'DECRBY', *args, shard_key=args[0])
        return self.execute(b'DECRBY', *args)

    def get(self, *args):
        """ Execute GET Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'GET', *args, shard_key=args[0])
        return self.execute(b'GET', *args)

    def getbit(self, *args):
        """ Execute GETBIT Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'GETBIT', *args, shard_key=args[0])
        return self.execute(b'GETBIT', *args)

    def getrange(self, *args):
        """ Execute GETRANGE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'GETRANGE', *args, shard_key=args[0])
        return self.execute(b'GETRANGE', *args)

    def getset(self, *args):
        """ Execute GETSET Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'GETSET', *args, shard_key=args[0])
        return self.execute(b'GETSET', *args)

    def incr(self, *args):
        """ Execute INCR Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'INCR', *args, shard_key=args[0])
        return self.execute(b'INCR', *args)

    def incrby(self, *args):
        """ Execute INCRBY Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'INCRBY', *args, shard_key=args[0])
        return self.execute(b'INCRBY', *args)

    def incrbyfloat(self, *args):
        """ Execute INCRBYFLOAT Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'INCRBYFLOAT', *args, shard_key=args[0])
        return self.execute(b'INCRBYFLOAT', *args)

    def mget(self, *args):
        """ Execute MGET Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'MGET', *args, shard_key=args[0])
        return self.execute(b'MGET', *args)

    def mset(self, *args):
        """ Execute MSET Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'MSET', *args, shard_key=args[0])
        return self.execute(b'MSET', *args)

    def msetnx(self, *args):
        """ Execute MSETNX Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'MSETNX', *args, shard_key=args[0])
        return self.execute(b'MSETNX', *args)

    def psetex(self, *args):
        """ Execute PSETEX Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'PSETEX', *args, shard_key=args[0])
        return self.execute(b'PSETEX', *args)

    def set(self, *args):
        """ Execute SET Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'SET', *args, shard_key=args[0])
        return self.execute(b'SET', *args)

    def setbit(self, *args):
        """ Execute SETBIT Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'SETBIT', *args, shard_key=args[0])
        return self.execute(b'SETBIT', *args)

    def setex(self, *args):
        """ Execute SETEX Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'SETEX', *args, shard_key=args[0])
        return self.execute(b'SETEX', *args)

    def setnx(self, *args):
        """ Execute SETNX Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'SETNX', *args, shard_key=args[0])
        return self.execute(b'SETNX', *args)

    def setrange(self, *args):
        """ Execute SETRANGE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'SETRANGE', *args, shard_key=args[0])
        return self.execute(b'SETRANGE', *args)

    def strlen(self, *args):
        """ Execute STRLEN Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'STRLEN', *args, shard_key=args[0])
        return self.execute(b'STRLEN', *args)


class Hash(BaseCommand):
    def __init__(self):
        super().__init__()

    def hdel(self, *args):
        """ Execute HDEL Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'HDEL', *args, shard_key=args[0])
        return self.execute(b'HDEL', *args)

    def hexists(self, *args):
        """ Execute HEXISTS Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'HEXISTS', *args, shard_key=args[0])
        return self.execute(b'HEXISTS', *args)

    def hget(self, *args):
        """ Execute HGET Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'HGET', *args, shard_key=args[0])
        return self.execute(b'HGET', *args)

    def hgetall(self, *args):
        """ Execute HGETALL Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'HGETALL', *args, shard_key=args[0])
        return self.execute(b'HGETALL', *args)

    def hincrby(self, *args):
        """ Execute HINCRBY Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'HINCRBY', *args, shard_key=args[0])
        return self.execute(b'HINCRBY', *args)

    def hincrbyfloat(self, *args):
        """ Execute HINCRBYFLOAT Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'HINCRBYFLOAT', *args, shard_key=args[0])
        return self.execute(b'HINCRBYFLOAT', *args)

    def hkeys(self, *args):
        """ Execute HKEYS Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'HKEYS', *args, shard_key=args[0])
        return self.execute(b'HKEYS', *args)

    def hlen(self, *args):
        """ Execute HLEN Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'HLEN', *args, shard_key=args[0])
        return self.execute(b'HLEN', *args)

    def hmget(self, *args):
        """ Execute HMGET Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'HMGET', *args, shard_key=args[0])
        return self.execute(b'HMGET', *args)

    def hmset(self, *args):
        """ Execute HMSET Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'HMSET', *args, shard_key=args[0])
        return self.execute(b'HMSET', *args)

    def hset(self, *args):
        """ Execute HSET Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'HSET', *args, shard_key=args[0])
        return self.execute(b'HSET', *args)

    def hsetnx(self, *args):
        """ Execute HSETNX Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'HSETNX', *args, shard_key=args[0])
        return self.execute(b'HSETNX', *args)

    def hstrlen(self, *args):
        """ Execute HSTRLEN Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'HSTRLEN', *args, shard_key=args[0])
        return self.execute(b'HSTRLEN', *args)

    def hvals(self, *args):
        """ Execute HVALS Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'HVALS', *args, shard_key=args[0])
        return self.execute(b'HVALS', *args)

    def hscan(self, *args):
        """ Execute HSCAN Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'HSCAN', *args, shard_key=args[0])
        return self.execute(b'HSCAN', *args)


class List(BaseCommand):
    def __init__(self):
        super().__init__()

    def blpop(self, *args):
        """ Execute BLPOP Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'BLPOP', *args, shard_key=args[0])
        return self.execute(b'BLPOP', *args)

    def brpop(self, *args):
        """ Execute BRPOP Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'BRPOP', *args, shard_key=args[0])
        return self.execute(b'BRPOP', *args)

    def brpoplpush(self, *args):
        """ Execute BRPOPPUSH Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'BRPOPPUSH', *args, shard_key=args[0])
        return self.execute(b'BRPOPPUSH', *args)

    def lindex(self, *args):
        """ Execute LINDEX Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'LINDEX', *args, shard_key=args[0])
        return self.execute(b'LINDEX', *args)

    def linsert(self, *args):
        """ Execute LINSERT Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'LINSERT', *args, shard_key=args[0])
        return self.execute(b'LINSERT', *args)

    def llen(self, *args):
        """ Execute LLEN Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'LLEN', *args, shard_key=args[0])
        return self.execute(b'LLEN', *args)

    def lpop(self, *args):
        """ Execute LPOP Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'LPOP', *args, shard_key=args[0])
        return self.execute(b'LPOP', *args)

    def lpush(self, *args):
        """ Execute LPUSH Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'LPUSH', *args, shard_key=args[0])
        return self.execute(b'LPUSH', *args)

    def lpushx(self, *args):
        """ Execute LPUSHX Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'LPUSHX', *args, shard_key=args[0])
        return self.execute(b'LPUSHX', *args)

    def lrange(self, *args):
        """ Execute LRANGE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'LRANGE', *args, shard_key=args[0])
        return self.execute(b'LRANGE', *args)

    def lrem(self, *args):
        """ Execute LREM Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'LREM', *args, shard_key=args[0])
        return self.execute(b'LREM', *args)

    def lset(self, *args):
        """ Execute LSET Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'LSET', *args, shard_key=args[0])
        return self.execute(b'LSET', *args)

    def ltrim(self, *args):
        """ Execute LTRIM Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'LTRIM', *args, shard_key=args[0])
        return self.execute(b'LTRIM', *args)

    def rpop(self, *args):
        """ Execute RPOP Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'RPOP', *args, shard_key=args[0])
        return self.execute(b'RPOP', *args)

    def rpoplpush(self, *args):
        """ Execute RPOPLPUSH Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'RPOPLPUSH', *args, shard_key=args[0])
        return self.execute(b'RPOPLPUSH', *args)

    def rpush(self, *args):
        """ Execute RPUSH Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'RPUSH', *args, shard_key=args[0])
        return self.execute(b'RPUSH', *args)

    def rpushx(self, *args):
        """ Execute RPUSHX Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'RPUSHX', *args, shard_key=args[0])
        return self.execute(b'RPUSHX', *args)


class Set(BaseCommand):
    def __init__(self):
        super().__init__()

    def sadd(self, *args):
        """ Execute SADD Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'SADD', *args, shard_key=args[0])
        return self.execute(b'SADD', *args)

    def scard(self, *args):
        """ Execute SCARD Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'SCARD', *args, shard_key=args[0])
        return self.execute(b'SCARD', *args)

    def sdiff(self, *args):
        """ Execute SDIFF Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'SDIFF', *args, shard_key=args[0])
        return self.execute(b'SDIFF', *args)

    def sdiffstore(self, *args):
        """ Execute SDIFFSTORE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'SDIFFSTORE', *args, shard_key=args[0])
        return self.execute(b'SDIFFSTORE', *args)

    def sinter(self, *args):
        """ Execute SINTER Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'SINTER', *args, shard_key=args[0])
        return self.execute(b'SINTER', *args)

    def sinterstore(self, *args):
        """ Execute SINTERSTORE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'SINTERSTORE', *args, shard_key=args[0])
        return self.execute(b'SINTERSTORE', *args)

    def sismember(self, *args):
        """ Execute SISMEMBER Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'SISMEMBER', *args, shard_key=args[0])
        return self.execute(b'SISMEMBER', *args)

    def smembers(self, *args):
        """ Execute SMEMBERS Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'SMEMBERS', *args, shard_key=args[0])
        return self.execute(b'SMEMBERS', *args)

    def smove(self, *args):
        """ Execute SMOVE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'SMOVE', *args, shard_key=args[0])
        return self.execute(b'SMOVE', *args)

    def spop(self, *args):
        """ Execute SPOP Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'SPOP', *args, shard_key=args[0])
        return self.execute(b'SPOP', *args)

    def srandmember(self, *args):
        """ Execute SRANDMEMBER Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'SRANDMEMBER', *args, shard_key=args[0])
        return self.execute(b'SRANDMEMBER', *args)

    def srem(self, *args):
        """ Execute SREM Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'SREM', *args, shard_key=args[0])
        return self.execute(b'SREM', *args)

    def sunion(self, *args):
        """ Execute SUNION Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'SUNION', *args, shard_key=args[0])
        return self.execute(b'SUNION', *args)

    def sunoinstore(self, *args):
        """ Execute SUNIONSTORE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'SUNIONSTORE', *args, shard_key=args[0])
        return self.execute(b'SUNIONSTORE', *args)

    def sscan(self, *args):
        """ Execute SSCAN Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'SSCAN', *args, shard_key=args[0])
        return self.execute(b'SSCAN', *args)


class SSet(BaseCommand):
    def __init__(self):
        super().__init__()

    def zadd(self, *args):
        """ Execute ZADD Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'ZADD', *args, shard_key=args[0])
        return self.execute(b'ZADD', *args)

    def zcard(self, *args):
        """ Execute ZCARD Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'ZCARD', *args, shard_key=args[0])
        return self.execute(b'ZCARD', *args)

    def zcount(self, *args):
        """ Execute ZCOUNT Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'ZCOUNT', *args, shard_key=args[0])
        return self.execute(b'ZCOUNT', *args)

    def zincrby(self, *args):
        """ Execute ZINCRBY Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'ZINCRBY', *args, shard_key=args[0])
        return self.execute(b'ZINCRBY', *args)

    def zinterstore(self, *args):
        """ Execute ZINTERSTORE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'ZINTERSTORE', *args, shard_key=args[0])
        return self.execute(b'ZINTERSTORE', *args)

    def zlexcount(self, *args):
        """ Execute ZLEXCOUNT Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'ZLEXCOUNT', *args, shard_key=args[0])
        return self.execute(b'ZLEXCOUNT', *args)

    def zrange(self, *args):
        """ Execute ZRANGE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'ZRANGE', *args, shard_key=args[0])
        return self.execute(b'ZRANGE', *args)

    def zrangebylex(self, *args):
        """ Execute ZRANGEBYLEX Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'ZRANGEBYLEX', *args, shard_key=args[0])
        return self.execute(b'ZRANGEBYLEX', *args)

    def zrangebyscore(self, *args):
        """ Execute ZRANGEBYSCORE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'ZRANGEBYSCORE', *args, shard_key=args[0])
        return self.execute(b'ZRANGEBYSCORE', *args)

    def zrank(self, *args):
        """ Execute ZRANK Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'ZRANK', *args, shard_key=args[0])
        return self.execute(b'ZRANK', *args)

    def zrem(self, *args):
        """ Execute ZREM Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'ZREM', *args, shard_key=args[0])
        return self.execute(b'ZREM', *args)

    def zremrangebylex(self, *args):
        """ Execute ZREMRANGEBYLEX Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'ZREMRANGEBYLEX', *args, shard_key=args[0])
        return self.execute(b'ZREMRANGEBYLEX', *args)

    def zremrangebyrank(self, *args):
        """ Execute ZREMRANGEBYRANK Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'ZREMRANGEBYRANK', *args, shard_key=args[0])
        return self.execute(b'ZREMRANGEBYRANK', *args)

    def zremrangebyscrore(self, *args):
        """ Execute ZREMRANGEBYSCORE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'ZREMRANGEBYSCORE', *args, shard_key=args[0])
        return self.execute(b'ZREMRANGEBYSCORE', *args)

    def zrevrange(self, *args):
        """ Execute ZREVRANGE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'ZREVRANGE', *args, shard_key=args[0])
        return self.execute(b'ZREVRANGE', *args)

    def zrevrangebylex(self, *args):
        """ Execute ZREVRANGEBYLEX Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'ZREVRANGEBYLEX', *args, shard_key=args[0])
        return self.execute(b'ZREVRANGEBYLEX', *args)

    def zrevrangebyscore(self, *args):
        """ Execute ZREVRANGEBYSCORE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'ZREVRANGEBYSCORE', *args, shard_key=args[0])
        return self.execute(b'ZREVRANGEBYSCORE', *args)

    def zrevrank(self, *args):
        """ Execute ZREVRANK Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'ZREVRANK', *args, shard_key=args[0])
        return self.execute(b'ZREVRANK', *args)

    def zscore(self, *args):
        """ Execute ZSCORE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'ZSCORE', *args, shard_key=args[0])
        return self.execute(b'ZSCORE', *args)

    def zunionstore(self, *args):
        """ Execute ZUNIONSTORE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'ZUNIONSTORE', *args, shard_key=args[0])
        return self.execute(b'ZUNIONSTORE', *args)

    def zscan(self, *args):
        """ Execute ZSCAN Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'ZSCAN', *args, shard_key=args[0])
        return self.execute(b'ZSCAN', *args)


class HyperLogLog(BaseCommand):
    def __init__(self):
        super().__init__()

    def pfadd(self, *args):
        """ Execute PFADD Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'PFADD', *args, shard_key=args[0])
        return self.execute(b'PFADD', *args)

    def pfcount(self, *args):
        """ Execute PFCOUNT Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'PFCOUNT', *args, shard_key=args[0])
        return self.execute(b'PFCOUNT', *args)

    def pfmerge(self, *args):
        """ Execute PFMERGE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'PFMERGE', *args, shard_key=args[0])
        return self.execute(b'PFMERGE', *args)


class Publish(BaseCommand):
    def __init__(self):
        super().__init__()

    def publish(self, *args):
        """ Execute PUBLISH Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            raise NotImplemented
        return self.execute(b'PUBLISH', *args)


class Subscribe(object):
    def write(self, *args):
        raise NotImplemented

    def psubscribe(self, *args):
        """ Execute PSUBSCRIBE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.write(b'PSUBSCRIBE', *args)

    def punsubscribe(self, *args):
        """ Execute PUNSUBSCRIBE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.write(b'PUNSUBSCRIBE', *args)

    def subscribe(self, *args):
        """ Execute SUBSCRIBE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.write(b'SUBSCRIBE', *args)

    def unsubscribe(self, *args):
        """ Execute UNSUBSCRIBE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.write(b'UNSUBSCRIBE', *args)


class Transaction(BaseCommand):
    def __init__(self):
        super().__init__()

    def discard(self, *args, shard_key=None, sock=None):
        """ Execute DISCARD Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'DISCARD', *args, shard_key=shard_key, sock=sock)
        return self.execute(b'DISCARD', *args)

    def exec(self, *args, shard_key=None, sock=None):
        """ Execute EXEC Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'EXEC', *args, shard_key=shard_key, sock=sock)
        return self.execute(b'EXEC', *args)

    def multi(self, *args, shard_key=None, sock=None):
        """ Execute MULTI Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'MULTI', *args, shard_key=shard_key, sock=sock)
        return self.execute(b'MULTI', *args)

    def unwatch(self, *args, shard_key=None, sock=None):
        """ Execute UNWATCH Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'UNWATCH', *args, shard_key=shard_key, sock=sock)
        return self.execute(b'UNWATCH', *args)

    def watch(self, *args):
        """ Execute WATCH Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'WATCH', *args, shard_key=args[0])
        return self.execute(b'WATCH', *args)


class Scripting(BaseCommand):
    def __init__(self):
        super().__init__()

    def eval(self, *args, shard_key=None, sock=None):
        """ Execute EVAL Command, consult Redis documentation for details.

        :param shard_key: (optional)
            Should be set to the key name you try to work with.
            Can not be used if sock is set.

            Only used if used with a Cluster Client
        :type shard_key: string

        :param sock: (optional)
            The string representation of a socket, the command should be executed against.
            For example: "testhost_6379"
            Can not be used if shard_key is set.

            Only used if used with a Cluster Client
        :type sock: string

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'EVAL', *args, shard_key=shard_key, sock=sock)
        return self.execute(b'EVAL', *args)

    def evalsha(self, *args, shard_key=None, sock=None):
        """ Execute EVALSHA Command, consult Redis documentation for details.

        :param shard_key: (optional)
            Should be set to the key name you try to work with.
            Can not be used if sock is set.

            Only used if used with a Cluster Client
        :type shard_key: string

        :param sock: (optional)
            The string representation of a socket, the command should be executed against.
            For example: "testhost_6379"
            Can not be used if shard_key is set.

            Only used if used with a Cluster Client
        :type sock: string

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'EVALSHA', *args, shard_key=shard_key, sock=sock)
        return self.execute(b'EVALSHA', *args)

    def script_debug(self, *args, shard_key=None, sock=None):
        """ Execute SCRIPT DEBUG Command, consult Redis documentation for details.

        :param shard_key: (optional)
            Should be set to the key name you try to work with.
            Can not be used if sock is set.

            Only used if used with a Cluster Client
        :type shard_key: string

        :param sock: (optional)
            The string representation of a socket, the command should be executed against.
            For example: "testhost_6379"
            Can not be used if shard_key is set.

            Only used if used with a Cluster Client
        :type sock: string

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'SCRIPT', b'DEBUG', *args, shard_key=shard_key, sock=sock)
        return self.execute(b'SCRIPT', b'DEBUG', *args)

    def script_exists(self, *args, shard_key=None, sock=None):
        """ Execute SCRIPT EXISTS Command, consult Redis documentation for details.

        :param shard_key: (optional)
            Should be set to the key name you try to work with.
            Can not be used if sock is set.

            Only used if used with a Cluster Client
        :type shard_key: string

        :param sock: (optional)
            The string representation of a socket, the command should be executed against.
            For example: "testhost_6379"
            Can not be used if shard_key is set.

            Only used if used with a Cluster Client
        :type sock: string

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'SCRIPT', b'EXISTS', *args, shard_key=shard_key, sock=sock)
        return self.execute(b'SCRIPT', b'EXISTS', *args)

    def script_flush(self, *args, shard_key=None, sock=None):
        """ Execute SCRIPT FLUSH Command, consult Redis documentation for details.

        :param shard_key: (optional)
            Should be set to the key name you try to work with.
            Can not be used if sock is set.

            Only used if used with a Cluster Client
        :type shard_key: string

        :param sock: (optional)
            The string representation of a socket, the command should be executed against.
            For example: "testhost_6379"
            Can not be used if shard_key is set.

            Only used if used with a Cluster Client
        :type sock: string

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'SCRIPT', b'FLUSH', *args, shard_key=shard_key, sock=sock)
        return self.execute(b'SCRIPT', b'FLUSH', *args)

    def script_kill(self, *args, shard_key=None, sock=None):
        """ Execute SCRIPT KILL Command, consult Redis documentation for details.

        :param shard_key: (optional)
            Should be set to the key name you try to work with.
            Can not be used if sock is set.

            Only used if used with a Cluster Client
        :type shard_key: string

        :param sock: (optional)
            The string representation of a socket, the command should be executed against.
            For example: "testhost_6379"
            Can not be used if shard_key is set.

            Only used if used with a Cluster Client
        :type sock: string

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'SCRIPT', b'KILL', *args, shard_key=shard_key, sock=sock)
        return self.execute(b'SCRIPT', b'KILL', *args)

    def script_load(self, *args, shard_key=None, sock=None):
        """ Execute SCRIPT LOAD Command, consult Redis documentation for details.

        :param shard_key: (optional)
            Should be set to the key name you try to work with.
            Can not be used if sock is set.

            Only used if used with a Cluster Client
        :type shard_key: string

        :param sock: (optional)
            The string representation of a socket, the command should be executed against.
            For example: "testhost_6379"
            Can not be used if shard_key is set.

            Only used if used with a Cluster Client
        :type sock: string

        :return: result, exception
        """
        if self._cluster:
            return self.execute(b'SCRIPT', b'LOAD', *args, shard_key=shard_key, sock=sock)
        return self.execute(b'SCRIPT', b'LOAD', *args)
