from collections import deque
import pyredis.client
from pyredis.exceptions import PyRedisConnError


class SentinelClient(object):
    def __init__(self, sentinels, password=None, username=None):
        self._conn = None
        self._sentinels = deque(sentinels)
        self._password = password
        self._username = username

    def _sentinel_connect(self, sentinel):
        host, port = sentinel
        self._conn = pyredis.client.Connection(
            host=host,
            port=port,
            conn_timeout=0.1,
            sentinel=True,
            password=self._password,
            username=self._username,
        )
        try:
            self.execute("PING")
            return True
        except PyRedisConnError:
            self.close()
            return False

    def _sentinel_get(self):
        for sentinel in range(len(self._sentinels)):
            if self._sentinel_connect(self._sentinels[0]):
                return True
            else:
                self._sentinels.rotate(-1)
        raise PyRedisConnError("Could not connect to any sentinel")

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None

    @property
    def sentinels(self):
        return self._sentinels

    def execute(self, *args):
        if not self._conn:
            self._sentinel_get()
        self._conn.write(*args)
        return self._conn.read()

    def get_master(self, name):
        return pyredis.client.dict_from_list(
            self.execute(
                *["SENTINEL", "master", name]
            )
        )

    def get_masters(self):
        masters = self.execute(
            *["SENTINEL", "masters"]
        )
        result = []
        for master in masters:
            result.append(
                pyredis.client.dict_from_list(master)
            )
        return result

    def get_slaves(self, name):
        slaves = self.execute(
            *["SENTINEL", "slaves", name]
        )
        result = []
        for slave in slaves:
            result.append(
                pyredis.client.dict_from_list(slave)
            )
        return result

    def next_sentinel(self):
        self.close()
        self._sentinels.rotate(-1)
