from collections import deque
import pyredis.client
from pyredis.exceptions import PyRedisConnError


class SentinelClient(object):
    """
    Synchronous Redis Sentinel Client.

    Handles connectivity to Sentinel nodes and master/slave service discovery.
    """

    def __init__(self, sentinels, password=None, username=None):
        """
        Initialize the SentinelClient.

        Args:
            sentinels: List of (host, port) tuples representing the Sentinel nodes.
            password: Optional password for Sentinel authentication.
            username: Optional username for Sentinel ACL authentication.
        """
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
        """Close the active Sentinel connection."""
        if self._conn:
            self._conn.close()
            self._conn = None

    @property
    def sentinels(self):
        """Deque of configured Sentinel (host, port) node addresses."""
        return self._sentinels

    def execute(self, *args):
        """
        Execute a Sentinel command, automatically selecting an active Sentinel node.

        Args:
            *args: Command name and arguments.

        Returns:
            The Sentinel command response.
        """
        if not self._conn:
            self._sentinel_get()
        self._conn.write(*args)
        return self._conn.read()

    def get_master(self, name):
        """
        Get the master node configuration for the specified service name.

        Args:
            name: The service name of the Redis master.

        Returns:
            Dict containing the master's configuration.
        """
        return pyredis.client.dict_from_list(
            self.execute(
                *["SENTINEL", "master", name]
            )
        )

    def get_masters(self):
        """
        Get configurations for all monitored Redis master nodes.

        Returns:
            List of dicts containing configurations for all monitored masters.
        """
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
        """
        Get replication replica configurations for the specified master service name.

        Args:
            name: The service name of the Redis master.

        Returns:
            List of dicts containing replica configurations.
        """
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
        """Close the active connection and rotate the Sentinel node list."""
        self.close()
        self._sentinels.rotate(-1)
