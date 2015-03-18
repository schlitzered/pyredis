__author__ = 'schlitzer'

from collections import deque

from pyredis import commands
from pyredis.connection import Connection
from pyredis.exceptions import *
from pyredis.helper import dict_from_list


class Client(
    commands.Connection,
    commands.Hash,
    commands.HyperLogLog,
    commands.Key,
    commands.List,
    commands.Publish,
    commands.Scripting,
    commands.Set,
    commands.SSet,
    commands.String,
    commands.Transaction
):
    """ Base Client for Talking to Redis.

    Inherits the following Commmand classes:
      - commands.Connection,
      - commands.Hash,
      - commands.HyperLogLog,
      - commands.Key,
      - commands.List,
      - commands.Publish,
      - commands.Scripting,
      - commands.Set,
      - commands.SSet,
      - commands.String,
      - commands.Transaction


    :param kwargs:
        pyredis.Client takes the same arguments as pyredis.connection.Connection.
    """
    def __init__(self, **kwargs):
        self._conn = Connection(**kwargs)
        self._bulk = False
        self._bulk_keep = False
        self._bulk_results = None
        self._bulk_size = None
        self._bulk_size_current = None

    def _bulk_fetch(self):
        while self._bulk_size_current != 0:
            result = self._conn.read(raise_on_result_err=False)
            self._bulk_size_current -= 1
            if self._bulk_keep:
                self._bulk_results.append(result)

    def _execute_basic(self, *args):
        self._conn.write(*args)
        return self._conn.read()

    def _execute_bulk(self, *args):
        self._conn.write(*args)
        self._bulk_size_current += 1
        if self._bulk_size_current == self._bulk_size:
            self._bulk_fetch()

    @property
    def bulk(self):
        """ True if bulk mode is enabled.

        :return: bool
        """
        return self._bulk

    def bulk_start(self, bulk_size=5000, keep_results=True):
        """ Enable bulk mode

        Put the client into bulk mode. Instead of executing a command & waiting for
        the reply, all commands are send to Redis without fetching the result.
        The results get fetched whenever $bulk_size commands have been executed,
        which will also resets the counter.

        :param bulk_size:
            Number of commands to execute, before fetching results.
        :type bulk_size: int

        :param keep_results:
            If True, keep the results. The Results will be returned when calling bulk_stop.
        :type keep_results: bool

        :return: None
        """
        if self.bulk:
            raise PyRedisError("Already in bulk mode")
        self._bulk = True
        self._bulk_size = bulk_size
        self._bulk_size_current = 0
        if keep_results:
            self._bulk_results = []
            self._bulk_keep = True

    def bulk_stop(self):
        """ Stop bulk mode.

        All outstanding results from previous commands get fetched.
        If bulk_start was called with keep_results=True, return a list with all
        results from the executed commands.

        :return: None, list
        """
        if not self.bulk:
            raise PyRedisError("Not in bulk mode")
        self._bulk_fetch()
        results = self._bulk_results
        self._bulk = False
        self._bulk_keep = False
        self._bulk_results = None
        self._bulk_size = None
        self._bulk_size_current = None
        return results

    def close(self):
        """ Close client.

        :return: None
        """
        self._conn.close()

    @property
    def closed(self):
        """ Check if client is closed.

        :return: bool
        """
        return self._conn.closed

    def execute(self, *args):
        """ Execute arbitrary redis command.

        :param args:
        :type args: list, int, float

        :return: result, exception
        """
        if not self._bulk:
            return self._execute_basic(*args)
        else:
            self._execute_bulk(*args)


class ClusterClient(object):
    pass


class PubSubClient(commands.Subscribe):
    """ Pub/Sub Client.

    Subscribe part of the Redis Pub/Sub System.

    :param kwargs:
        pyredis.Client takes the same arguments as pyredis.connection.Connection.
    """
    def __init__(self, **kwargs):
        self._conn = Connection(**kwargs)

    def close(self):
        """ Close Client

        :return: None
        """
        self._conn.close()

    @property
    def closed(self):
        """ Check if Client is closed.

        :return: bool
        """
        return self._conn.closed

    def get(self):
        """ Fetch published item from Redis.

        :return: list
        """
        return self._conn.read(close_on_timeout=False)


class SentinelClient(object):
    """ Redis Sentinel Client.

    """
    def __init__(self, sentinels):
        self._conn = None
        self._sentinels = deque(sentinels)

    def _sentinel_connect(self, sentinel):
        host, port = sentinel
        self._conn = Connection(host=host, port=port, conn_timeout=0.1, sentinel=True)
        try:
            self.execute('PING')
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
        raise PyRedisConnError('Could not connect to any sentinel')

    def close(self):
        """ Close Connection.

        :return: None
        """
        if self._conn:
            self._conn.close()
            self._conn = None

    @property
    def sentinels(self):
        """ Return configured sentinels.

        :return: deque
        """
        return self._sentinels

    def execute(self, *args):
        """ Execute sentinel command.

        :param args:
        :type args: string, int, float

        :return: result, exception
        """
        if not self._conn:
            self._sentinel_get()
        self._conn.write(*args)
        return self._conn.read()

    def get_master(self, name):
        """ Get Master Info.

        Return dictionary with master details.

        :param name: Name of Redis service
        :type name: str

        :return: dict
        """
        return dict_from_list(self.execute('SENTINEL', 'master', name))

    def get_masters(self):
        """ Get list of masters.

        :return: list of dicts
        """
        masters = self.execute('SENTINEL', 'masters')
        result = []
        for master in masters:
            result.append(dict_from_list(master))
        return result

    def get_slaves(self, name):
        """ Get slaves.

        Return a list of dictionaries, with slave details.

        :param name: Name of Redis service
        :type name: str

        :return:
        """
        slaves = self.execute('SENTINEL', 'slaves', name)
        result = []
        for slave in slaves:
            result.append(dict_from_list(slave))
        return result

    def next_sentinel(self):
        """ Switch to the Next Sentinel.

        :return: None
        """
        self.close()
        self._sentinels.rotate(-1)