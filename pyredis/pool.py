__author__ = 'schlitzer'

from random import shuffle
import threading
from pyredis.client import Client, SentinelClient
from pyredis.exceptions import *


class BasePool(object):
    """ Base Class for all other pools.

    Other Pools Subclass from this Pool

    """
    def __init__(
            self,
            database=0,
            password=None,
            encoding=None,
            conn_timeout=2,
            read_timeout=2,
            pool_size=16,
            lock=threading.Lock()):
        self._conn_timeout = conn_timeout
        self._read_timeout = read_timeout
        self._lock = lock
        self._pool_free = set()
        self._pool_used = set()
        self._database = database
        self._password = password
        self._encoding = encoding
        self._pool_size = pool_size
        self._close_on_err = False

    @property
    def conn_timeout(self):
        return self._conn_timeout

    @property
    def read_timeout(self):
        return self._read_timeout

    @property
    def database(self):
        return self._database

    @property
    def password(self):
        return self._password

    @property
    def encoding(self):
        return self._encoding

    @property
    def pool_size(self):
        return self._pool_size

    @pool_size.setter
    def pool_size(self, size):
        self._pool_size = size

    @property
    def close_on_err(self):
        return self._close_on_err

    def _connect(self):
        raise NotImplemented

    def acquire(self):
        try:
            self._lock.acquire()
            client = self._pool_free.pop()
            self._pool_used.add(client)
        except KeyError:
            if len(self._pool_used) < self.pool_size:
                client = self._connect()
                self._pool_used.add(client)
            else:
                raise PyRedisError('Max connections {0} exhausted'.format(self.pool_size))
        finally:
            self._lock.release()
        return client

    def release(self, conn):
        try:
            self._lock.acquire()
            self._pool_used.remove(conn)
            if conn.closed and self.close_on_err:
                for conn in self._pool_free:
                    conn.close()
                self._pool_free = set()
                self._pool_used = set()
            elif not conn.closed:
                self._pool_free.add(conn)
        except KeyError:
            conn.close()
        finally:
            self._lock.release()


class Pool(BasePool):
    def __init__(self, host=None, port=6379, unix_sock=None, **kwargs):
        if not bool(host) != bool(unix_sock):
            raise PyRedisError("Ether host or unix_sock has to be provided")
        super().__init__(**kwargs)
        self._host = host
        self._port = port
        self._unix_sock = unix_sock

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def unix_sock(self):
        return self._unix_sock

    def _connect(self):
        return Client(
            host=self.host,
            port=self.port,
            unix_sock=self.unix_sock,
            database=self.database,
            password=self.password,
            encoding=self.encoding,
            conn_timeout=self.conn_timeout,
            read_timeout=self.read_timeout
            )


class SentinelPool(BasePool):
    def __init__(self, sentinels, name, slave_ok=False, retries=3, **kwargs):
        super().__init__(**kwargs)
        self._sentinel = SentinelClient(sentinels=sentinels)
        self._name = name
        self._slave_ok = slave_ok
        self._retries = retries
        self._close_on_err = True

    @property
    def slave_ok(self):
        return self._slave_ok

    @property
    def name(self):
        return self._name

    @property
    def retries(self):
        return self._retries

    @property
    def sentinels(self):
        return self._sentinel.sentinels

    def _connect(self):
        for _ in range(self.retries):
            if self.slave_ok:
                client = self._get_slave()
            else:
                client = self._get_master()
            if client:
                return client
        raise PyRedisConnError("Could not connect to Redis")

    def _get_client(self, host, port):
        return Client(
            host=host,
            port=port,
            database=self.database,
            password=self.password,
            encoding=self.encoding,
            conn_timeout=self.conn_timeout,
            read_timeout=self.read_timeout
        )

    def _get_master(self):
        candidate = self._sentinel.get_master(self.name)
        host = candidate[b'ip']
        port = int(candidate[b'port'])
        client = self._get_client(host, port)
        state = client.execute('INFO', 'replication')
        if b'role:master' in state:
            return client
        else:
            client.close()
            self._sentinel.next_sentinel()

    def _get_slave(self):
        candidates = []
        for candidate in self._sentinel.get_slaves(self.name):
            candidates.append((candidate[b'ip'], int(candidate[b'port'])))
        shuffle(candidates)
        for candidate in candidates:
            host = candidate[0]
            port = candidate[1]
            client = self._get_client(host, port)
            state = client.execute('INFO', 'replication')
            if b'role:slave' in state:
                return client
            else:
                client.close()
        self._sentinel.next_sentinel()