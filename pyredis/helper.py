import crc16
import random
from collections import deque
from threading import Lock
from uuid import uuid4

from pyredis.connection import Connection
from pyredis.exceptions import PyRedisError
from pyredis.protocol import to_bytes


def dict_from_list(source):
    return dict(zip(*[iter(source)]*2))


def tag_from_key(key):
    """ return tag from key

    Tries to convert key to bytes, and return the string
    enclosed by '{' and '}', if any.
    If there is no pair of curly braces enclosing a string,
    the key, converted to bytes, is returned.

    :param key: str, bytes
    :return: bytes
    """
    key = to_bytes(key)
    lcb = key.find(b'{')
    rcb = key.find(b'}')
    if not (lcb >= 0 and rcb >= 0):
        return key
    else:
        return key[lcb+1:rcb]


def slot_from_key(key):
    return crc16.crc16xmodem(tag_from_key(key)) % 16384


class ClusterMap(object):
    def __init__(self, seeds, lock=Lock()):
        self._id = uuid4()
        self._lock = lock
        self._map = {}
        self._seeds = deque(seeds)

    @property
    def id(self):
        return self._id

    @staticmethod
    def _make_str(endpoint):
        return str(endpoint[0])+'_'+str(endpoint[1])

    def _fetch_map(self):
        for seed in self._seeds:
            conn = Connection(host=seed[0], port=seed[1], encoding='utf-8')
            try:
                conn.write('CLUSTER', 'SLOTS')
                return conn.read()
            except PyRedisError:
                pass
            finally:
                conn.close()
        raise PyRedisError('Could not get cluster info from any seed node: {0}'.format(self._seeds))

    def _update_slot(self, slot, master, slaves):
        self._map[slot] = {
            'master': self._make_str(master),
            'slave': self._make_str(random.choice(slaves))
        }

    def get_slot(self, shard_key, slave=None):
        if not slave:
            return self._map[slot_from_key(shard_key)]['master']
        else:
            return self._map[slot_from_key(shard_key)]['slave']

    def hosts(self, slave=None):
        result = set()
        if not slave:
            selector = 'master'
        else:
            selector = 'slave'
        for host in self._map.values():
            result.add(host[selector])
        return result

    def update(self, id):
        with self._lock:
            if id != self.id:
                return self.id
            for entry in self._fetch_map():
                for slot in range(entry[0], entry[1]+1):
                    self._update_slot(slot, entry[2], entry[3:])
            self._id = uuid4()
            return self.id

