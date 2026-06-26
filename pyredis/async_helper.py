import asyncio
import random
from collections import deque
from uuid import uuid4

from pyredis.connection import AsyncConnection
from pyredis.exceptions import PyRedisError
from pyredis.helper import slot_from_key


class AsyncClusterMap(object):
    def __init__(
        self,
        seeds,
        password=None,
        lock=None,
        username=None,
    ):
        self._id = uuid4()
        if lock is None:
            self._lock = asyncio.Lock()
        else:
            self._lock = lock
        self._map = {}
        self._seeds = deque(seeds)
        self._password = password
        self._username = username

    @property
    def id(self):
        return self._id

    @staticmethod
    def _make_str(endpoint):
        return str(endpoint[0]) + "_" + str(endpoint[1])

    async def _fetch_map(self):
        for seed in self._seeds:
            conn = AsyncConnection(
                host=seed[0],
                port=seed[1],
                encoding="utf-8",
                password=self._password,
                username=self._username,
            )
            try:
                await conn.write(
                    *["CLUSTER", "SLOTS"]
                )
                return await conn.read()
            except PyRedisError:
                pass
            finally:
                await conn.close()
        raise PyRedisError(
            "Could not get cluster info from any seed node: "
            "{0}".format(self._seeds)
        )

    def _update_slot(
        self,
        slot,
        master,
        slaves
    ):
        self._map[slot] = {
            "master": self._make_str(master),
            "slave": self._make_str(random.choice(slaves)),
        }

    def get_slot(
        self,
        shard_key,
        slave=None
    ):
        if not slave:
            return self._map[slot_from_key(shard_key)]["master"]
        else:
            return self._map[slot_from_key(shard_key)]["slave"]

    def hosts(
        self,
        slave=None
    ):
        result = set()
        if not slave:
            selector = "master"
        else:
            selector = "slave"
        for host in self._map.values():
            result.add(host[selector])
        return result

    async def update(self, map_id):
        async with self._lock:
            if map_id != self.id:
                return self.id
            slots = await self._fetch_map()
            for entry in slots:
                for slot in range(
                    entry[0],
                    entry[1] + 1
                ):
                    self._update_slot(
                        slot=slot,
                        master=entry[2],
                        slaves=entry[3:]
                    )
            self._id = uuid4()
            return self.id
