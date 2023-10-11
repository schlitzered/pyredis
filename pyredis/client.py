from collections import deque

from pyredis import commands
from pyredis.connection import Connection
from pyredis.exceptions import PyRedisError
from pyredis.exceptions import PyRedisConnError
from pyredis.exceptions import PyRedisConnReadTimeout
from pyredis.exceptions import ReplyError
from pyredis.helper import dict_from_list
from pyredis.helper import ClusterMap
from pyredis.helper import slot_from_key


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
    commands.Transaction,
):
    """Base Client for Talking to Redis.

    Inherits the following Command classes:
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
        super().__init__()
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
        """True if bulk mode is enabled.

        :return: bool
        """
        return self._bulk

    def bulk_start(self, bulk_size=5000, keep_results=True):
        """Enable bulk mode

        Put the client into bulk mode. Instead of executing a command & waiting for
        the reply, all commands are send to Redis without fetching the result.
        The results get fetched whenever $bulk_size commands have been executed,
        which will also resets the counter, or of bulk_stop() is called.

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
        """Stop bulk mode.

        All outstanding results from previous commands get fetched.
        If bulk_start was called with keep_results=True, return a list with all
        results from the executed commands in order. The list of results can also contain
        Exceptions, hat you should check for.

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
        """Close client.

        :return: None
        """
        self._conn.close()

    @property
    def closed(self):
        """Check if client is closed.

        :return: bool
        """
        return self._conn.closed

    def execute(self, *args):
        """Execute arbitrary redis command.

        :param args:
        :type args: list, int, float

        :return: result, exception
        """
        if not self._bulk:
            return self._execute_basic(*args)
        else:
            self._execute_bulk(*args)


class ClusterClient(
    commands.Connection,
    commands.Hash,
    commands.HyperLogLog,
    commands.Key,
    commands.List,
    commands.Scripting,
    commands.Set,
    commands.SSet,
    commands.String,
    commands.Transaction,
):
    """Base Client for Talking to Redis Cluster.

    Inherits the following Commmand classes:
      - commands.Connection,
      - commands.Hash,
      - commands.HyperLogLog,
      - commands.Key,
      - commands.List,
      - commands.Scripting,
      - commands.Set,
      - commands.SSet,
      - commands.String,
      - commands.Transaction

    :param seeds:
        Accepts a list of seed nodes in this form: [('seed1', 6379), ('seed2', 6379), ('seed3', 6379)]
    :type seeds: list

    :param slave_ok:
        Set to True if this Client should use slave nodes.
    :type slave_ok: bool

    :param database:
        Select which db should be used for this connection
    :type database: int

    :param password:
        Password used for authentication. If None, no authentication is done
    :type password: str

    :param encoding:
        Convert result strings with this encoding. If None, no encoding is done.
    :type encoding: str

    :param conn_timeout:
        Connect Timeout.
    :type conn_timeout: float

    :param read_timeout:
        Read Timeout.
    :type read_timeout: float

    :param username:
        Username used for acl scl authentication. If not set, fall back use legacy auth.
    :type username: str
    """

    def __init__(
        self,
        seeds=None,
        database=0,
        password=None,
        encoding=None,
        slave_ok=False,
        conn_timeout=2,
        read_timeout=2,
        cluster_map=None,
        username=None,
    ):
        super().__init__()
        if not bool(seeds) != bool(cluster_map):
            raise PyRedisError("Ether seeds or cluster_map has to be provided")
        self._cluster = True
        self._conns = dict()
        self._conn_timeout = conn_timeout
        self._read_timeout = read_timeout
        self._encoding = encoding
        self._password = password
        self._database = database
        self._slave_ok = slave_ok
        if cluster_map:
            self._map = cluster_map
        else:
            self._map = ClusterMap(seeds=seeds)
        self._map_id = self._map.id
        self._username = username

    def _cleanup_conns(self):
        hosts = self._map.hosts(slave=self._slave_ok)
        wipe = set()
        for conn in self._conns.keys():
            if conn not in hosts:
                wipe.add(conn)

        for conn in wipe:
            self._conns[conn].close()
            del self._conns[conn]

    def _connect(self, sock):
        host, port = sock.split("_")
        client = Connection(
            host=host,
            port=int(port),
            conn_timeout=self._conn_timeout,
            read_timeout=self._read_timeout,
            read_only=self._slave_ok,
            encoding=self._encoding,
            password=self._password,
            database=self._database,
            username=self._username,
        )
        self._conns[sock] = client

    def _get_slot_info(self, shard_key):
        if self._map_id != self._map.id:
            self._map_id = self._map.id
            self._cleanup_conns()
        try:
            return self._map.get_slot(shard_key, self._slave_ok)
        except KeyError:
            self._map_id = self._map.update(self._map_id)
            self._cleanup_conns()
            return self._map.get_slot(shard_key, self._slave_ok)

    @property
    def closed(self):
        return False

    def execute(self, *args, shard_key=None, sock=None, asking=False, retries=3):
        """Execute arbitrary redis command.

        :param args:
        :type args: list, int, float

        :param shard_key: (optional)
            Should be set to the key name you try to work with.
            Can not be used if sock is set.
        :type shard_key: string

        :param sock: (optional)
            The string representation of a socket, the command should be executed against.
            For example: "testhost_6379"
            Can not be used if shard_key is set.
        :type sock: string

        :return: result, exception
        """
        if not bool(shard_key) != bool(sock):
            raise PyRedisError("Ether shard_key or sock has to be provided")
        if not sock:
            sock = self._get_slot_info(shard_key)
        if sock not in self._conns.keys():
            self._connect(sock)
        try:
            if asking:
                self._conns[sock].write("ASKING", *args)
            else:
                self._conns[sock].write(*args)
            return self._conns[sock].read()
        except ReplyError as err:
            errstr = str(err)
            if retries <= 1 and (
                errstr.startswith("MOVED") or errstr.startswith("ASK")
            ):
                raise PyRedisError("Slot moved to often or wrong shard_key, giving up,")
            if errstr.startswith("MOVED"):
                if not shard_key:
                    raise ReplyError(
                        "Explicitly set socket, but key does not belong to this redis: {0}".format(
                            sock
                        )
                    )
                self._map_id = self._map.update(self._map_id)
                self._cleanup_conns()
                return self.execute(*args, shard_key=shard_key, retries=retries - 1)
            elif errstr.startswith("ASK"):
                sock = errstr.split()[2].replace(":", "_")
                return self.execute(*args, sock=sock, retries=retries - 1, asking=True)
            else:
                raise err
        except (PyRedisConnError, PyRedisConnReadTimeout) as err:
            self._conns[sock].close()
            del self._conns[sock]
            self._map.update(self._map_id)
            raise err


class HashClient(
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
    commands.Transaction,
):
    """Client for Talking to Static Hashed Redis Cluster.

    The Client will calculate a crc16 hash using the shard_key,
    which is be default the first Key in case the command supports multiple keys.
    If the Key is using the TAG annotation "bla{tag}blarg",
    then only the tag portion is used, in this case "tag".
    The key space is split into 16384 buckets, so in theory you could provide
    a list with 16384 ('host', port) pairs to the "buckets" parameter.
    If you have less then 16384 ('host', port) pairs, the client will try to
    distribute the key spaces evenly between available pairs.

    --- Warning ---
    Since this is static hashing, the order of pairs has to match on each client you use!
    Also changing the number of pairs will change the mapping between buckets and pairs,
    rendering your data inaccessible!

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
    """

    def __init__(
        self,
        buckets,
        database=None,
        password=None,
        encoding=None,
        conn_timeout=2,
        read_timeout=2,
        username=None,
    ):
        super().__init__()
        self._conns = dict()
        self._conn_names = list()
        self._bulk = False
        self._bulk_keep = False
        self._bulk_results = None
        self._bulk_size = None
        self._bulk_size_current = None
        self._bulk_bucket_order = list()
        self._closed = False
        self._cluster = True
        self._map = dict()
        self._init_conns(
            buckets=buckets,
            database=database,
            password=password,
            encoding=encoding,
            conn_timeout=conn_timeout,
            read_timeout=read_timeout,
            username=username,
        )
        self._init_map()

    def _bulk_fetch(self):
        for conn in self._bulk_bucket_order:
            result = conn.read(raise_on_result_err=False)
            if self._bulk_keep:
                self._bulk_results.append(result)
        self._bulk_bucket_order = list()
        self._bulk_size_current = 0

    @staticmethod
    def _execute_basic(*args, conn):
        conn.write(*args)
        return conn.read()

    def _execute_bulk(self, *args, conn):
        conn.write(*args)
        self._bulk_size_current += 1
        self._bulk_bucket_order.append(conn)
        if self._bulk_size_current == self._bulk_size:
            self._bulk_fetch()

    def _init_conns(
        self,
        buckets,
        database,
        password,
        encoding,
        conn_timeout,
        read_timeout,
        username,
    ):
        for bucket in buckets:
            host, port = bucket
            bucketname = "{0}_{1}".format(host, port)
            self._conn_names.append(bucketname)
            self._conns[bucketname] = Connection(
                host=host,
                port=port,
                database=database,
                password=password,
                encoding=encoding,
                conn_timeout=conn_timeout,
                read_timeout=read_timeout,
                username=username,
            )

    def _init_map(self):
        num_buckets = len(self._conn_names) - 1
        cur_bucket = 0
        for slot in range(16384):
            self._map[slot] = self._conn_names[cur_bucket]
            if cur_bucket == num_buckets:
                cur_bucket = 0
            else:
                cur_bucket += 1

    @property
    def bulk(self):
        """True if bulk mode is enabled.

        :return: bool
        """
        return self._bulk

    def bulk_start(self, bulk_size=5000, keep_results=True):
        """Enable bulk mode

        Put the client into bulk mode. Instead of executing a command & waiting for
        the reply, all commands are send to Redis without fetching the result.
        The results get fetched whenever $bulk_size commands have been executed,
        which will also resets the counter, or of bulk_stop() is called.

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
        """Stop bulk mode.

        All outstanding results from previous commands get fetched.
        If bulk_start was called with keep_results=True, return a list with all
        results from the executed commands in order. The list of results can also contain
        Exceptions, hat you should check for.

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
        """Close client.

        :return: None
        """
        for conn in self._conns.values():
            conn.close()
        self._closed = True

    @property
    def closed(self):
        """Check if client is closed.

        :return: bool
        """
        return self._closed

    def execute(self, *args, shard_key=None, sock=None):
        """Execute arbitrary redis command.

        :param args:
        :type args: list, int, float

        :param shard_key: (optional)
            Should be set to the key name you try to work with.
            Can not be used if sock is set.
        :type shard_key: string

        :param sock: (optional)
            The string representation of a socket, the command should be executed against.
            For example: "testhost_6379"
            Can not be used if shard_key is set.
        :type sock: string

        :return: result, exception
        """
        if not bool(shard_key) != bool(sock):
            raise PyRedisError("Ether shard_key or sock has to be provided")
        if not sock:
            sock = self._map[slot_from_key(shard_key)]
        conn = self._conns[sock]
        try:
            if not self._bulk:
                return self._execute_basic(conn=conn, *args)
            else:
                self._execute_bulk(conn=conn, *args)
        except PyRedisConnError as err:
            self.close()
            raise err


class PubSubClient(commands.Subscribe):
    """Pub/Sub Client.

    Subscribe part of the Redis Pub/Sub System.

    :param kwargs:
        pyredis.PubSubClient takes the same arguments as pyredis.connection.Connection.
    """

    def __init__(self, **kwargs):
        self._conn = Connection(**kwargs)

    def close(self):
        """Close Client

        :return: None
        """
        self._conn.close()

    @property
    def closed(self):
        """Check if Client is closed.

        :return: bool
        """
        return self._conn.closed

    def write(self, *args):
        return self._conn.write(*args)

    def get(self):
        """Fetch published item from Redis.

        :return: list
        """
        return self._conn.read(close_on_timeout=False)


class SentinelClient(object):
    """Redis Sentinel Client.

    :param sentinels:
        Accepts a list of sentinels in this form: [('sentinel1', 26379), ('sentinel2', 26379), ('sentinel3', 26379)]
    :type sentinels: list

    :param password:
        Password used for authentication of Sentinel instance itself. If None, no authentication is done.
        Only available starting with Redis 5.0.1.
    :type password: str

    :param username:
        Username used for acl scl authentication. If not set, fall back use legacy auth.
    :type username: str
    """

    def __init__(self, sentinels, password=None, username=None):
        self._conn = None
        self._sentinels = deque(sentinels)
        self._password = password
        self._username = username

    def _sentinel_connect(self, sentinel):
        host, port = sentinel
        self._conn = Connection(
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
        """Close Connection.

        :return: None
        """
        if self._conn:
            self._conn.close()
            self._conn = None

    @property
    def sentinels(self):
        """Return configured sentinels.

        :return: deque
        """
        return self._sentinels

    def execute(self, *args):
        """Execute sentinel command.

        :param args:
        :type args: string, int, float

        :return: result, exception
        """
        if not self._conn:
            self._sentinel_get()
        self._conn.write(*args)
        return self._conn.read()

    def get_master(self, name):
        """Get Master Info.

        Return dictionary with master details.

        :param name: Name of Redis service
        :type name: str

        :return: dict
        """
        return dict_from_list(self.execute("SENTINEL", "master", name))

    def get_masters(self):
        """Get list of masters.

        :return: list of dicts
        """
        masters = self.execute("SENTINEL", "masters")
        result = []
        for master in masters:
            result.append(dict_from_list(master))
        return result

    def get_slaves(self, name):
        """Get slaves.

        Return a list of dictionaries, with slave details.

        :param name: Name of Redis service
        :type name: str

        :return:
        """
        slaves = self.execute("SENTINEL", "slaves", name)
        result = []
        for slave in slaves:
            result.append(dict_from_list(slave))
        return result

    def next_sentinel(self):
        """Switch to the Next Sentinel.

        :return: None
        """
        self.close()
        self._sentinels.rotate(-1)
