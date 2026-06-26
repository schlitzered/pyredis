from collections import deque
import pyredis.client
from pyredis.exceptions import PyRedisConnError


class AsyncSentinelClient(object):
    """
    Asynchronous Redis Sentinel Client.

    Handles connectivity to Sentinel nodes and master/slave service discovery asynchronously.
    """

    def __init__(self, sentinels, password=None, username=None):
        """
        Initialize the AsyncSentinelClient.

        Args:
            sentinels: List of (host, port) tuples representing the Sentinel nodes.
            password: Optional password for Sentinel authentication.
            username: Optional username for Sentinel ACL authentication.
        """
        self._conn = None
        self._sentinels = deque(sentinels)
        self._password = password
        self._username = username

    async def _sentinel_connect(self, sentinel):
        host, port = sentinel
        self._conn = pyredis.client.AsyncConnection(
            host=host,
            port=port,
            conn_timeout=0.1,
            sentinel=True,
            password=self._password,
            username=self._username,
        )
        try:
            await self.execute("PING")
            return True
        except PyRedisConnError:
            await self.close()
            return False

    async def _sentinel_get(self):
        for sentinel in range(len(self._sentinels)):
            if await self._sentinel_connect(self._sentinels[0]):
                return True
            else:
                self._sentinels.rotate(-1)
        raise PyRedisConnError("Could not connect to any sentinel")

    async def close(self):
        """Close the active Sentinel connection asynchronously."""
        if self._conn:
            await self._conn.close()
            self._conn = None

    @property
    def sentinels(self):
        """Deque of configured Sentinel (host, port) node addresses."""
        return self._sentinels

    async def execute(self, *args):
        """
        Execute a Sentinel command asynchronously, automatically selecting an active Sentinel node.

        Args:
            *args: Command name and arguments.

        Returns:
            The Sentinel command response.
        """
        if not self._conn:
            await self._sentinel_get()
        await self._conn.write(*args)
        return await self._conn.read()

    async def get_master(self, name):
        """
        Get the master node configuration for the specified service name asynchronously.

        Args:
            name: The service name of the Redis master.

        Returns:
            Dict containing the master's configuration.
        """
        result = await self.execute(
            *["SENTINEL", "master", name]
        )
        return pyredis.client.dict_from_list(result)

    async def get_masters(self):
        """
        Get configurations for all monitored Redis master nodes asynchronously.

        Returns:
            List of dicts containing configurations for all monitored masters.
        """
        masters = await self.execute(
            *["SENTINEL", "masters"]
        )
        result = []
        for master in masters:
            result.append(
                pyredis.client.dict_from_list(master)
            )
        return result

    async def get_slaves(self, name):
        """
        Get replication replica configurations for the specified master service name asynchronously.

        Args:
            name: The service name of the Redis master.

        Returns:
            List of dicts containing replica configurations.
        """
        slaves = await self.execute(
            *["SENTINEL", "slaves", name]
        )
        result = []
        for slave in slaves:
            result.append(
                pyredis.client.dict_from_list(slave)
            )
        return result

    async def next_sentinel(self):
        """Close the active connection and rotate the Sentinel node list asynchronously."""
        await self.close()
        self._sentinels.rotate(-1)
