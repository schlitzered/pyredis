__author__ = 'schlitzer'

__all__ = [
    'Connection'
]


class Connection(object):
    def echo(self, *args):
        """ Execute ECHO Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('ECHO', *args)

    def ping(self):
        """ Execute PING Command, consult Redis documentation for details.

        :return: result,exception
        """
        return self.execute('PING')


class Key(object):
    def delete(self, *args):
        """ Execute DEL Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('DEL', *args)

    def dump(self, *args):
        """ Execute DUMP Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('DUMP', *args)

    def exists(self, *args):
        """ Execute EXISTS Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('EXISTS', *args)

    def expire(self, *args):
        """ Execute EXPIRE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('EXPIRE', *args)

    def expireat(self, *args):
        """ Execute EXPIREAT Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('EXPIREAT', *args)

    def keys(self, *args):
        """ Execute KEYS Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('KEYS', *args)

    def migrate(self, *args):
        """ Execute MIGRATE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('MIGRATE', *args)

    def move(self, *args):
        """ Execute MOVE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('MOVE', *args)

    def object(self, *args):
        """ Execute OBJECT Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('OBJECT', *args)

    def persist(self, *args):
        """ Execute PERSIST Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('PERSIST', *args)

    def pexpire(self, *args):
        """ Execute PEXPIRE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('PEXPIRE', *args)

    def pexpireat(self, *args):
        """ Execute PEXPIREAT Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('PEXPIREAT', *args)

    def pttl(self, *args):
        """ Execute PTTL Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('PTTL', *args)

    def randomkey(self, *args):
        """ Execute RANDOMKEY Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('RANDOMKEY', *args)

    def rename(self, *args):
        """ Execute RENAME Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('RENAME', *args)

    def renamenx(self, *args):
        """ Execute RENAMENX Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('RENAMENX', *args)

    def restore(self, *args):
        """ Execute RESTORE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('RESTORE', *args)

    def sort(self, *args):
        """ Execute SORT Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('SORT', *args)

    def ttl(self, *args):
        """ Execute TTL Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('TTL', *args)

    def type(self, *args):
        """ Execute TYPE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('TYPE', *args)

    def scan(self, *args):
        """ Execute SCAN Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('SCAN', *args)


class String(object):
    def append(self, *args):
        """ Execute APPEND Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('APPEND', *args)

    def bitcount(self, *args):
        """ Execute BITCOUNT Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('BITCOUNT', *args)

    def bitop(self, *args):
        """ Execute BITOP Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('BITOP', *args)

    def bitpos(self, *args):
        """ Execute BITPOS Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('BITPOS', *args)

    def decr(self, *args):
        """ Execute DECR Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('DECR', *args)

    def decrby(self, *args):
        """ Execute DECRBY Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('DECRBY', *args)

    def get(self, *args):
        """ Execute GET Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('GET', *args)

    def getbit(self, *args):
        """ Execute GETBIT Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('GETBIT', *args)

    def getrange(self, *args):
        """ Execute GETRANGE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('GETRANGE', *args)

    def getset(self, *args):
        """ Execute GETSET Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('GETSET', *args)

    def incr(self, *args):
        """ Execute INCR Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('INCR', *args)

    def incrby(self, *args):
        """ Execute INCRBY Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('INCRBY', *args)

    def incrbyfloat(self, *args):
        """ Execute INCRBYFLOAT Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('INCRBYFLOAT', *args)

    def mget(self, *args):
        """ Execute MGET Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('MGET', *args)

    def mset(self, *args):
        """ Execute MSET Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('MSET', *args)

    def msetnx(self, *args):
        """ Execute MSETNX Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('MSETNX', *args)

    def psetex(self, *args):
        """ Execute PSETEX Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('PSETEX', *args)

    def set(self, *args):
        """ Execute SET Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('SET', *args)

    def setbit(self, *args):
        """ Execute SETBIT Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('SETBIT', *args)

    def setex(self, *args):
        """ Execute SETEX Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('SETEX', *args)

    def setnx(self, *args):
        """ Execute SETNX Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('SETNX', *args)

    def setrange(self, *args):
        """ Execute SETRANGE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('SETRANGE', *args)

    def strlen(self, *args):
        """ Execute STRLEN Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('STRLEN', *args)


class Hash(object):
    def hdel(self, *args):
        """ Execute HDEL Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('HDEL', *args)

    def hexists(self, *args):
        """ Execute HEXISTS Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('HEXISTS', *args)

    def hget(self, *args):
        """ Execute HGET Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('HGET', *args)

    def hgetall(self, *args):
        """ Execute HGETALL Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('HGETALL', *args)

    def hincrby(self, *args):
        """ Execute HINCRBY Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('HINCRBY', *args)

    def hincrbyfloat(self, *args):
        """ Execute HINCRBYFLOAT Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('HINCRBYFLOAT', *args)

    def hkeys(self, *args):
        """ Execute HKEYS Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('HKEYS', *args)

    def hlen(self, *args):
        """ Execute HLEN Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('HLEN', *args)

    def hmget(self, *args):
        """ Execute HMGET Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('HMGET', *args)

    def hmset(self, *args):
        """ Execute HMSET Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('HMSET', *args)

    def hset(self, *args):
        """ Execute HSET Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('HSET', *args)

    def hsetnx(self, *args):
        """ Execute HSETNX Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('HSETNX', *args)

    def hvals(self, *args):
        """ Execute HVALS Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('HVALS', *args)

    def hscan(self, *args):
        """ Execute HSCAN Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('HSCAN', *args)


class List(object):
    def blpop(self, *args):
        """ Execute BLPOP Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('BLPOP', *args)

    def brpop(self, *args):
        """ Execute BRPOP Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('BRPOP', *args)

    def brpoplpush(self, *args):
        """ Execute BRPOPPUSH Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('BRPOPPUSH', *args)

    def lindex(self, *args):
        """ Execute LINDEX Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('LINDEX', *args)

    def linsert(self, *args):
        """ Execute LINSERT Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('LINSERT', *args)

    def llen(self, *args):
        """ Execute LLEN Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('LLEN', *args)

    def lpop(self, *args):
        """ Execute LPOP Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('LPOP', *args)

    def lpush(self, *args):
        """ Execute LPUSH Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('LPUSH', *args)

    def lpushx(self, *args):
        """ Execute LPUSHX Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('LPUSHX', *args)

    def lrange(self, *args):
        """ Execute LRANGE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('LRANGE', *args)

    def lrem(self, *args):
        """ Execute LREM Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('LREM', *args)

    def lset(self, *args):
        """ Execute LSET Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('LSET', *args)

    def ltrim(self, *args):
        """ Execute LTRIM Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('LTRIM', *args)

    def rpop(self, *args):
        """ Execute RPOP Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('RPOP', *args)

    def rpoplpush(self, *args):
        """ Execute RPOPLPUSH Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('RPOPLPUSH', *args)

    def rpush(self, *args):
        """ Execute RPUSH Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('RPUSH', *args)

    def rpushx(self, *args):
        """ Execute RPUSHX Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('RPUSHX', *args)


class Set(object):
    def sadd(self, *args):
        """ Execute SADD Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('SADD', *args)

    def scard(self, *args):
        """ Execute SCARD Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('SCARD', *args)

    def sdiff(self, *args):
        """ Execute SDIFF Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('SDIFF', *args)

    def sdiffstore(self, *args):
        """ Execute SDIFFSTORE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('SDIFFSTORE', *args)

    def sinter(self, *args):
        """ Execute SINTER Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('SINTER', *args)

    def sinterstore(self, *args):
        """ Execute SINTERSTORE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('SINTERSTORE', *args)

    def sismember(self, *args):
        """ Execute SISMEMBER Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('SISMEMBER', *args)

    def smembers(self, *args):
        """ Execute SMEMBERS Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('SMEMBERS', *args)

    def smove(self, *args):
        """ Execute SMOVE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('SMOVE', *args)

    def spop(self, *args):
        """ Execute SPOP Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('SPOP', *args)

    def srandmember(self, *args):
        """ Execute SRANDMEMBER Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('SRANDMEMBER', *args)

    def srem(self, *args):
        """ Execute SREM Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('SREM', *args)

    def sunion(self, *args):
        """ Execute SUNION Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('SUNION', *args)

    def sunoinstore(self, *args):
        """ Execute SUNIONSTORE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('SUNIONSTORE', *args)

    def sscan(self, *args):
        """ Execute SSCAN Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('SSCAN', *args)


class SSet(object):
    def zadd(self, *args):
        """ Execute ZADD Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('ZADD', *args)

    def zcard(self, *args):
        """ Execute ZCARD Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('ZCARD', *args)

    def zcount(self, *args):
        """ Execute ZCOUNT Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('ZCOUNT', *args)

    def zincrby(self, *args):
        """ Execute ZINCRBY Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('ZINCRBY', *args)

    def zinterstore(self, *args):
        """ Execute ZINTERSTORE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('ZINTERSTORE', *args)

    def zlexcount(self, *args):
        """ Execute ZLEXCOUNT Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('ZLEXCOUNT', *args)

    def zrange(self, *args):
        """ Execute ZRANGE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('ZRANGE', *args)

    def zrangebylex(self, *args):
        """ Execute ZRANGEBYLEX Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('ZRANGEBYLEX', *args)

    def zrangebyscore(self, *args):
        """ Execute ZRANGEBYSCORE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('ZRANGEBYSCORE', *args)

    def zrank(self, *args):
        """ Execute ZRANK Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('ZRANK', *args)

    def zrem(self, *args):
        """ Execute ZREM Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('ZREM', *args)

    def zremrangebylex(self, *args):
        """ Execute ZREMRANGEBYLEX Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('ZREMRANGEBYLEX', *args)

    def zremrangebyrank(self, *args):
        """ Execute ZREMRANGEBYRANK Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('ZREMRANGEBYRANK', *args)

    def zremrangebyscrore(self, *args):
        """ Execute ZREMRANGEBYSCORE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('ZREMRANGEBYSCORE', *args)

    def zrevrange(self, *args):
        """ Execute ZREVRANGE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('ZREVRANGE', *args)

    def zrevrangebyscore(self, *args):
        """ Execute ZREVRANGEBYSCORE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('ZREVRANGEBYSCORE', *args)

    def zrevrank(self, *args):
        """ Execute ZREVRANK Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('ZREVRANK', *args)

    def zscore(self, *args):
        """ Execute ZSCORE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('ZSCORE', *args)

    def zunionstore(self, *args):
        """ Execute ZUNIONSTORE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('ZUNIONSTORE', *args)

    def zscan(self, *args):
        """ Execute ZSCAN Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('ZSCAN', *args)


class HyperLogLog(object):
    def pfadd(self, *args):
        """ Execute PFADD Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('PFADD', *args)

    def pfcount(self, *args):
        """ Execute PFCOUNT Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('PFCOUNT', *args)

    def pfmerge(self, *args):
        """ Execute PFMERGE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('PFMERGE', *args)


class Publish(object):
    def publish(self, *args):
        """ Execute PUBLISH Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('PUBLISH', *args)


class Subscribe(object):
    def psubscribe(self, *args):
        """ Execute PSUBSCRIBE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self._conn.write('PSUBSCRIBE', *args)

    def punsubscribe(self, *args):
        """ Execute PUNSUBSCRIBE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self._conn.write('PUNSUBSCRIBE', *args)

    def subscribe(self, *args):
        """ Execute SUBSCRIBE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self._conn.write('SUBSCRIBE', *args)

    def unsubscribe(self, *args):
        """ Execute UNSUBSCRIBE Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self._conn.write('UNSUBSCRIBE', *args)


class Transaction(object):
    def discard(self, *args):
        """ Execute DISCARD Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('DISCARD', *args)

    def exec(self, *args):
        """ Execute EXEC Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('EXEC', *args)

    def multi(self, *args):
        """ Execute MULTI Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('MULTI', *args)

    def unwatch(self, *args):
        """ Execute UNWATCH Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('UNWATCH', *args)

    def watch(self, *args):
        """ Execute WATCH Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('WATCH', *args)


class Scripting(object):
    def eval(self, *args):
        """ Execute EVAL Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('EVAL', *args)

    def evalsha(self, *args):
        """ Execute EVALSHA Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('EVALSHA', *args)

    def script_exists(self, *args):
        """ Execute SCRIPT EXISTS Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('SCRIPT', 'EXISTS', *args)

    def script_flush(self, *args):
        """ Execute SCRIPT FLUSH Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('SCRIPT', 'FLUSH', *args)

    def script_kill(self, *args):
        """ Execute SCRIPT KILL Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('SCRIPT', 'KILL', *args)

    def script_load(self, *args):
        """ Execute SCRIPT LOAD Command, consult Redis documentation for details.

        :return: result, exception
        """
        return self.execute('SCRIPT', 'LOAD', *args)
