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
            return self.execute('ECHO', *args, shard_key=shard_key, sock=sock)
        return self.execute('ECHO', *args)

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
            return self.execute('PING', shard_key=shard_key, sock=sock)
        return self.execute('PING')


class Geo(BaseCommand):
    def __init__(self):
        super().__init__()

    def geoadd(self, *args):
        """ Execute GEOADD Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('GEOADD', *args, shard_key=args[0])
        return self.execute('GEOADD', *args)

    def geodist(self, *args):
        """ Execute GEODIST Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('GEODIST', *args, shard_key=args[0])
        return self.execute('GEODIST', *args)

    def geohash(self, *args):
        """ Execute GEOHASH Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('GEOHASH', *args, shard_key=args[0])
        return self.execute('GEOHASH', *args)

    def georadius(self, *args):
        """ Execute GEORADIUS Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('GEORADIUS', *args, shard_key=args[0])
        return self.execute('GEORADIUS', *args)

    def geopos(self, *args):
        """ Execute GEOPOS Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('GEOPOS', *args, shard_key=args[0])
        return self.execute('GEOPOS', *args)

    def georadiusbymember(self, *args):
        """ Execute GEORADIUSBYMEMBER Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('GEORADIUSBYMEMBER', *args, shard_key=args[0])
        return self.execute('GEORADIUSBYMEMBER', *args)


class Key(BaseCommand):
    def __init__(self):
        super().__init__()

    def delete(self, *args):
        """ Execute DEL Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('DEL', *args, shard_key=args[0])
        return self.execute('DEL', *args)

    def dump(self, *args):
        """ Execute DUMP Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('DUMP', *args, shard_key=args[0])
        return self.execute('DUMP', *args)

    def exists(self, *args):
        """ Execute EXISTS Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('EXISTS', *args, shard_key=args[0])
        return self.execute('EXISTS', *args)

    def expire(self, *args):
        """ Execute EXPIRE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('EXPIRE', *args, shard_key=args[0])
        return self.execute('EXPIRE', *args)

    def expireat(self, *args):
        """ Execute EXPIREAT Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('EXPIREAT')
        return self.execute('EXPIREAT', *args)

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
            return self.execute('KEYS', *args, shard_key=shard_key, sock=sock)
        return self.execute('KEYS', *args)

    def migrate(self, *args):
        """ Execute MIGRATE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            raise NotImplemented
        return self.execute('MIGRATE', *args)

    def move(self, *args):
        """ Execute MOVE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('MOVE', *args, shard_key=args[0])
        return self.execute('MOVE', *args)

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
            return self.execute('DEL', *args, shard_key=shard_key, sock=sock)
        return self.execute('OBJECT', *args)

    def persist(self, *args):
        """ Execute PERSIST Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('PERSIST', *args, shard_key=args[0])
        return self.execute('PERSIST', *args)

    def pexpire(self, *args):
        """ Execute PEXPIRE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('PEXPIRE', *args, shard_key=args[0])
        return self.execute('PEXPIRE', *args)

    def pexpireat(self, *args):
        """ Execute PEXPIREAT Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('PEXPIREAT', *args, shard_key=args[0])
        return self.execute('PEXPIREAT', *args)

    def pttl(self, *args):
        """ Execute PTTL Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('PTTL', *args, shard_key=args[0])
        return self.execute('PTTL', *args)

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
            return self.execute('RANDOMKEY', *args, shard_key=shard_key, sock=sock)
        return self.execute('RANDOMKEY', *args)

    def rename(self, *args):
        """ Execute RENAME Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('RENAME', *args, shard_key=args[0])
        return self.execute('RENAME', *args)

    def renamenx(self, *args):
        """ Execute RENAMENX Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('RENAMENX', *args, shard_key=args[0])
        return self.execute('RENAMENX', *args)

    def restore(self, *args):
        """ Execute RESTORE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('RESTORE', *args, shard_key=args[0])
        return self.execute('RESTORE', *args)

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
            return self.execute('SCAN', *args, shard_key=shard_key, sock=sock)
        return self.execute('SCAN', *args)

    def sort(self, *args):
        """ Execute SORT Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('SORT', *args, shard_key=args[0])
        return self.execute('SORT', *args)

    def ttl(self, *args):
        """ Execute TTL Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('TTL', *args, shard_key=args[0])
        return self.execute('TTL', *args)

    def type(self, *args):
        """ Execute TYPE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('TYPE', *args, shard_key=args[0])
        return self.execute('TYPE', *args)

    def wait(self, *args):
        """ Execute WAIT Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('WAIT', *args, shard_key=args[0])
        return self.execute('WAIT', *args)


class String(BaseCommand):
    def __init__(self):
        super().__init__()

    def append(self, *args):
        """ Execute APPEND Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('APPEND', *args, shard_key=args[0])
        return self.execute('APPEND', *args)

    def bitcount(self, *args):
        """ Execute BITCOUNT Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('BITCOUNT', *args, shard_key=args[0])
        return self.execute('BITCOUNT', *args)

    def bitfield(self, *args):
        """ Execute BITFIELD Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('BITFIELD', *args, shard_key=args[0])
        return self.execute('BITFIELD', *args)

    def bitop(self, *args):
        """ Execute BITOP Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('BITOP', *args, shard_key=args[1])
        return self.execute('BITOP', *args)

    def bitpos(self, *args):
        """ Execute BITPOS Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('BITPOS', *args, shard_key=args[0])
        return self.execute('BITPOS', *args)

    def decr(self, *args):
        """ Execute DECR Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('DECR', *args, shard_key=args[0])
        return self.execute('DECR', *args)

    def decrby(self, *args):
        """ Execute DECRBY Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('DECRBY', *args, shard_key=args[0])
        return self.execute('DECRBY', *args)

    def get(self, *args):
        """ Execute GET Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('GET', *args, shard_key=args[0])
        return self.execute('GET', *args)

    def getbit(self, *args):
        """ Execute GETBIT Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('GETBIT', *args, shard_key=args[0])
        return self.execute('GETBIT', *args)

    def getrange(self, *args):
        """ Execute GETRANGE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('GETRANGE', *args, shard_key=args[0])
        return self.execute('GETRANGE', *args)

    def getset(self, *args):
        """ Execute GETSET Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('GETSET', *args, shard_key=args[0])
        return self.execute('GETSET', *args)

    def incr(self, *args):
        """ Execute INCR Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('INCR', *args, shard_key=args[0])
        return self.execute('INCR', *args)

    def incrby(self, *args):
        """ Execute INCRBY Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('INCRBY', *args, shard_key=args[0])
        return self.execute('INCRBY', *args)

    def incrbyfloat(self, *args):
        """ Execute INCRBYFLOAT Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('INCRBYFLOAT', *args, shard_key=args[0])
        return self.execute('INCRBYFLOAT', *args)

    def mget(self, *args):
        """ Execute MGET Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('MGET', *args, shard_key=args[0])
        return self.execute('MGET', *args)

    def mset(self, *args):
        """ Execute MSET Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('MSET', *args, shard_key=args[0])
        return self.execute('MSET', *args)

    def msetnx(self, *args):
        """ Execute MSETNX Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('MSETNX', *args, shard_key=args[0])
        return self.execute('MSETNX', *args)

    def psetex(self, *args):
        """ Execute PSETEX Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('PSETEX', *args, shard_key=args[0])
        return self.execute('PSETEX', *args)

    def set(self, *args):
        """ Execute SET Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('SET', *args, shard_key=args[0])
        return self.execute('SET', *args)

    def setbit(self, *args):
        """ Execute SETBIT Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('SETBIT', *args, shard_key=args[0])
        return self.execute('SETBIT', *args)

    def setex(self, *args):
        """ Execute SETEX Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('SETEX', *args, shard_key=args[0])
        return self.execute('SETEX', *args)

    def setnx(self, *args):
        """ Execute SETNX Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('SETNX', *args, shard_key=args[0])
        return self.execute('SETNX', *args)

    def setrange(self, *args):
        """ Execute SETRANGE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('SETRANGE', *args, shard_key=args[0])
        return self.execute('SETRANGE', *args)

    def strlen(self, *args):
        """ Execute STRLEN Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('STRLEN', *args, shard_key=args[0])
        return self.execute('STRLEN', *args)


class Hash(BaseCommand):
    def __init__(self):
        super().__init__()

    def hdel(self, *args):
        """ Execute HDEL Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('HDEL', *args, shard_key=args[0])
        return self.execute('HDEL', *args)

    def hexists(self, *args):
        """ Execute HEXISTS Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('HEXISTS', *args, shard_key=args[0])
        return self.execute('HEXISTS', *args)

    def hget(self, *args):
        """ Execute HGET Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('HGET', *args, shard_key=args[0])
        return self.execute('HGET', *args)

    def hgetall(self, *args):
        """ Execute HGETALL Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('HGETALL', *args, shard_key=args[0])
        return self.execute('HGETALL', *args)

    def hincrby(self, *args):
        """ Execute HINCRBY Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('HINCRBY', *args, shard_key=args[0])
        return self.execute('HINCRBY', *args)

    def hincrbyfloat(self, *args):
        """ Execute HINCRBYFLOAT Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('HINCRBYFLOAT', *args, shard_key=args[0])
        return self.execute('HINCRBYFLOAT', *args)

    def hkeys(self, *args):
        """ Execute HKEYS Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('HKEYS', *args, shard_key=args[0])
        return self.execute('HKEYS', *args)

    def hlen(self, *args):
        """ Execute HLEN Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('HLEN', *args, shard_key=args[0])
        return self.execute('HLEN', *args)

    def hmget(self, *args):
        """ Execute HMGET Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('HMGET', *args, shard_key=args[0])
        return self.execute('HMGET', *args)

    def hmset(self, *args):
        """ Execute HMSET Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('HMSET', *args, shard_key=args[0])
        return self.execute('HMSET', *args)

    def hset(self, *args):
        """ Execute HSET Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('HSET', *args, shard_key=args[0])
        return self.execute('HSET', *args)

    def hsetnx(self, *args):
        """ Execute HSETNX Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('HSETNX', *args, shard_key=args[0])
        return self.execute('HSETNX', *args)

    def hstrlen(self, *args):
        """ Execute HSTRLEN Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('HSTRLEN', *args, shard_key=args[0])
        return self.execute('HSTRLEN', *args)

    def hvals(self, *args):
        """ Execute HVALS Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('HVALS', *args, shard_key=args[0])
        return self.execute('HVALS', *args)

    def hscan(self, *args):
        """ Execute HSCAN Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('HSCAN', *args, shard_key=args[0])
        return self.execute('HSCAN', *args)


class List(BaseCommand):
    def __init__(self):
        super().__init__()

    def blpop(self, *args):
        """ Execute BLPOP Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('BLPOP', *args, shard_key=args[0])
        return self.execute('BLPOP', *args)

    def brpop(self, *args):
        """ Execute BRPOP Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('BRPOP', *args, shard_key=args[0])
        return self.execute('BRPOP', *args)

    def brpoplpush(self, *args):
        """ Execute BRPOPPUSH Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('BRPOPPUSH', *args, shard_key=args[0])
        return self.execute('BRPOPPUSH', *args)

    def lindex(self, *args):
        """ Execute LINDEX Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('LINDEX', *args, shard_key=args[0])
        return self.execute('LINDEX', *args)

    def linsert(self, *args):
        """ Execute LINSERT Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('LINSERT', *args, shard_key=args[0])
        return self.execute('LINSERT', *args)

    def llen(self, *args):
        """ Execute LLEN Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('LLEN', *args, shard_key=args[0])
        return self.execute('LLEN', *args)

    def lpop(self, *args):
        """ Execute LPOP Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('LPOP', *args, shard_key=args[0])
        return self.execute('LPOP', *args)

    def lpush(self, *args):
        """ Execute LPUSH Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('LPUSH', *args, shard_key=args[0])
        return self.execute('LPUSH', *args)

    def lpushx(self, *args):
        """ Execute LPUSHX Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('LPUSHX', *args, shard_key=args[0])
        return self.execute('LPUSHX', *args)

    def lrange(self, *args):
        """ Execute LRANGE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('LRANGE', *args, shard_key=args[0])
        return self.execute('LRANGE', *args)

    def lrem(self, *args):
        """ Execute LREM Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('LREM', *args, shard_key=args[0])
        return self.execute('LREM', *args)

    def lset(self, *args):
        """ Execute LSET Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('LSET', *args, shard_key=args[0])
        return self.execute('LSET', *args)

    def ltrim(self, *args):
        """ Execute LTRIM Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('LTRIM', *args, shard_key=args[0])
        return self.execute('LTRIM', *args)

    def rpop(self, *args):
        """ Execute RPOP Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('RPOP', *args, shard_key=args[0])
        return self.execute('RPOP', *args)

    def rpoplpush(self, *args):
        """ Execute RPOPLPUSH Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('RPOPLPUSH', *args, shard_key=args[0])
        return self.execute('RPOPLPUSH', *args)

    def rpush(self, *args):
        """ Execute RPUSH Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('RPUSH', *args, shard_key=args[0])
        return self.execute('RPUSH', *args)

    def rpushx(self, *args):
        """ Execute RPUSHX Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('RPUSHX', *args, shard_key=args[0])
        return self.execute('RPUSHX', *args)


class Set(BaseCommand):
    def __init__(self):
        super().__init__()

    def sadd(self, *args):
        """ Execute SADD Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('SADD', *args, shard_key=args[0])
        return self.execute('SADD', *args)

    def scard(self, *args):
        """ Execute SCARD Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('SCARD', *args, shard_key=args[0])
        return self.execute('SCARD', *args)

    def sdiff(self, *args):
        """ Execute SDIFF Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('SDIFF', *args, shard_key=args[0])
        return self.execute('SDIFF', *args)

    def sdiffstore(self, *args):
        """ Execute SDIFFSTORE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('SDIFFSTORE', *args, shard_key=args[0])
        return self.execute('SDIFFSTORE', *args)

    def sinter(self, *args):
        """ Execute SINTER Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('SINTER', *args, shard_key=args[0])
        return self.execute('SINTER', *args)

    def sinterstore(self, *args):
        """ Execute SINTERSTORE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('SINTERSTORE', *args, shard_key=args[0])
        return self.execute('SINTERSTORE', *args)

    def sismember(self, *args):
        """ Execute SISMEMBER Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('SISMEMBER', *args, shard_key=args[0])
        return self.execute('SISMEMBER', *args)

    def smembers(self, *args):
        """ Execute SMEMBERS Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('SMEMBERS', *args, shard_key=args[0])
        return self.execute('SMEMBERS', *args)

    def smove(self, *args):
        """ Execute SMOVE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('SMOVE', *args, shard_key=args[0])
        return self.execute('SMOVE', *args)

    def spop(self, *args):
        """ Execute SPOP Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('SPOP', *args, shard_key=args[0])
        return self.execute('SPOP', *args)

    def srandmember(self, *args):
        """ Execute SRANDMEMBER Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('SRANDMEMBER', *args, shard_key=args[0])
        return self.execute('SRANDMEMBER', *args)

    def srem(self, *args):
        """ Execute SREM Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('SREM', *args, shard_key=args[0])
        return self.execute('SREM', *args)

    def sunion(self, *args):
        """ Execute SUNION Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('SUNION', *args, shard_key=args[0])
        return self.execute('SUNION', *args)

    def sunoinstore(self, *args):
        """ Execute SUNIONSTORE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('SUNIONSTORE', *args, shard_key=args[0])
        return self.execute('SUNIONSTORE', *args)

    def sscan(self, *args):
        """ Execute SSCAN Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('SSCAN', *args, shard_key=args[0])
        return self.execute('SSCAN', *args)


class SSet(BaseCommand):
    def __init__(self):
        super().__init__()

    def zadd(self, *args):
        """ Execute ZADD Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('ZADD', *args, shard_key=args[0])
        return self.execute('ZADD', *args)

    def zcard(self, *args):
        """ Execute ZCARD Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('ZCARD', *args, shard_key=args[0])
        return self.execute('ZCARD', *args)

    def zcount(self, *args):
        """ Execute ZCOUNT Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('ZCOUNT', *args, shard_key=args[0])
        return self.execute('ZCOUNT', *args)

    def zincrby(self, *args):
        """ Execute ZINCRBY Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('ZINCRBY', *args, shard_key=args[0])
        return self.execute('ZINCRBY', *args)

    def zinterstore(self, *args):
        """ Execute ZINTERSTORE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('ZINTERSTORE', *args, shard_key=args[0])
        return self.execute('ZINTERSTORE', *args)

    def zlexcount(self, *args):
        """ Execute ZLEXCOUNT Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('ZLEXCOUNT', *args, shard_key=args[0])
        return self.execute('ZLEXCOUNT', *args)

    def zrange(self, *args):
        """ Execute ZRANGE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('ZRANGE', *args, shard_key=args[0])
        return self.execute('ZRANGE', *args)

    def zrangebylex(self, *args):
        """ Execute ZRANGEBYLEX Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('ZRANGEBYLEX', *args, shard_key=args[0])
        return self.execute('ZRANGEBYLEX', *args)

    def zrangebyscore(self, *args):
        """ Execute ZRANGEBYSCORE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('ZRANGEBYSCORE', *args, shard_key=args[0])
        return self.execute('ZRANGEBYSCORE', *args)

    def zrank(self, *args):
        """ Execute ZRANK Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('ZRANK', *args, shard_key=args[0])
        return self.execute('ZRANK', *args)

    def zrem(self, *args):
        """ Execute ZREM Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('ZREM', *args, shard_key=args[0])
        return self.execute('ZREM', *args)

    def zremrangebylex(self, *args):
        """ Execute ZREMRANGEBYLEX Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('ZREMRANGEBYLEX', *args, shard_key=args[0])
        return self.execute('ZREMRANGEBYLEX', *args)

    def zremrangebyrank(self, *args):
        """ Execute ZREMRANGEBYRANK Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('ZREMRANGEBYRANK', *args, shard_key=args[0])
        return self.execute('ZREMRANGEBYRANK', *args)

    def zremrangebyscrore(self, *args):
        """ Execute ZREMRANGEBYSCORE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('ZREMRANGEBYSCORE', *args, shard_key=args[0])
        return self.execute('ZREMRANGEBYSCORE', *args)

    def zrevrange(self, *args):
        """ Execute ZREVRANGE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('ZREVRANGE', *args, shard_key=args[0])
        return self.execute('ZREVRANGE', *args)

    def zrevrangebylex(self, *args):
        """ Execute ZREVRANGEBYLEX Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('ZREVRANGEBYLEX', *args, shard_key=args[0])
        return self.execute('ZREVRANGEBYLEX', *args)

    def zrevrangebyscore(self, *args):
        """ Execute ZREVRANGEBYSCORE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('ZREVRANGEBYSCORE', *args, shard_key=args[0])
        return self.execute('ZREVRANGEBYSCORE', *args)

    def zrevrank(self, *args):
        """ Execute ZREVRANK Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('ZREVRANK', *args, shard_key=args[0])
        return self.execute('ZREVRANK', *args)

    def zscore(self, *args):
        """ Execute ZSCORE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('ZSCORE', *args, shard_key=args[0])
        return self.execute('ZSCORE', *args)

    def zunionstore(self, *args):
        """ Execute ZUNIONSTORE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('ZUNIONSTORE', *args, shard_key=args[0])
        return self.execute('ZUNIONSTORE', *args)

    def zscan(self, *args):
        """ Execute ZSCAN Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('ZSCAN', *args, shard_key=args[0])
        return self.execute('ZSCAN', *args)


class HyperLogLog(BaseCommand):
    def __init__(self):
        super().__init__()

    def pfadd(self, *args):
        """ Execute PFADD Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('PFADD', *args, shard_key=args[0])
        return self.execute('PFADD', *args)

    def pfcount(self, *args):
        """ Execute PFCOUNT Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('PFCOUNT', *args, shard_key=args[0])
        return self.execute('PFCOUNT', *args)

    def pfmerge(self, *args):
        """ Execute PFMERGE Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('PFMERGE', *args, shard_key=args[0])
        return self.execute('PFMERGE', *args)


class Publish(BaseCommand):
    def __init__(self):
        super().__init__()

    def publish(self, *args):
        """ Execute PUBLISH Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            raise NotImplemented
        return self.execute('PUBLISH', *args)


class Subscribe(object):
    def write(self, *args):
        raise NotImplemented

    def psubscribe(self, *args):
        """ Execute PSUBSCRIBE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.write('PSUBSCRIBE', *args)

    def punsubscribe(self, *args):
        """ Execute PUNSUBSCRIBE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.write('PUNSUBSCRIBE', *args)

    def subscribe(self, *args):
        """ Execute SUBSCRIBE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.write('SUBSCRIBE', *args)

    def unsubscribe(self, *args):
        """ Execute UNSUBSCRIBE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.write('UNSUBSCRIBE', *args)


class Transaction(BaseCommand):
    def __init__(self):
        super().__init__()

    def discard(self, *args, shard_key=None, sock=None):
        """ Execute DISCARD Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('DISCARD', *args, shard_key=shard_key, sock=sock)
        return self.execute('DISCARD', *args)

    def exec(self, *args, shard_key=None, sock=None):
        """ Execute EXEC Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('EXEC', *args, shard_key=shard_key, sock=sock)
        return self.execute('EXEC', *args)

    def multi(self, *args, shard_key=None, sock=None):
        """ Execute MULTI Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('MULTI', *args, shard_key=shard_key, sock=sock)
        return self.execute('MULTI', *args)

    def unwatch(self, *args, shard_key=None, sock=None):
        """ Execute UNWATCH Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('UNWATCH', *args, shard_key=shard_key, sock=sock)
        return self.execute('UNWATCH', *args)

    def watch(self, *args):
        """ Execute WATCH Command, consult Redis documentation for details.

        :return: result, exception
        """
        if self._cluster:
            return self.execute('WATCH', *args, shard_key=args[0])
        return self.execute('WATCH', *args)


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
            return self.execute('EVAL', *args, shard_key=shard_key, sock=sock)
        return self.execute('EVAL', *args)

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
            return self.execute('EVALSHA', *args, shard_key=shard_key, sock=sock)
        return self.execute('EVALSHA', *args)

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
            return self.execute('SCRIPT', 'DEBUG', *args, shard_key=shard_key, sock=sock)
        return self.execute('SCRIPT', 'DEBUG', *args)

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
            return self.execute('SCRIPT', 'EXISTS', *args, shard_key=shard_key, sock=sock)
        return self.execute('SCRIPT', 'EXISTS', *args)

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
            return self.execute('SCRIPT', 'FLUSH', *args, shard_key=shard_key, sock=sock)
        return self.execute('SCRIPT', 'FLUSH', *args)

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
            return self.execute('SCRIPT', 'KILL', *args, shard_key=shard_key, sock=sock)
        return self.execute('SCRIPT', 'KILL', *args)

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
            return self.execute('SCRIPT', 'LOAD', *args, shard_key=shard_key, sock=sock)
        return self.execute('SCRIPT', 'LOAD', *args)
