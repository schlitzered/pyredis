from pyredis import commands
import pyredis.client
from pyredis.exceptions import PyRedisConnError
from pyredis.exceptions import PyRedisConnReadTimeout
from pyredis.exceptions import PyRedisError
from pyredis.exceptions import ReplyError


class ClusterClient(
    commands.Connection,
    commands.Geo,
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
    """
    Synchronous Redis Cluster Client.

    Automatically routes Redis commands to appropriate cluster nodes
    by tracking keyspace slots via a ClusterMap. Handles MOVED and ASK redirection.
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
            self._map = pyredis.client.ClusterMap(seeds=seeds)
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
        client = pyredis.client.Connection(
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
            return self._map.get_slot(
                shard_key=shard_key,
                slave=self._slave_ok
            )
        except KeyError:
            self._map_id = self._map.update(self._map_id)
            self._cleanup_conns()
            return self._map.get_slot(
                shard_key=shard_key,
                slave=self._slave_ok
            )

    @property
    def closed(self):
        return False

    def execute(
        self,
        *args,
        shard_key=None,
        sock=None,
        asking=False,
        retries=3
    ):
        if not bool(shard_key) != bool(sock):
            raise PyRedisError("Ether shard_key or sock has to be provided")
        if not sock:
            sock = self._get_slot_info(shard_key)
        if sock not in self._conns.keys():
            self._connect(sock)
        try:
            if asking:
                self._conns[sock].write(
                    *["ASKING", *args]
                )
            else:
                self._conns[sock].write(*args)
            return self._conns[sock].read()
        except ReplyError as err:
            errstr = str(err)
            if retries <= 1 and (
                errstr.startswith("MOVED") or errstr.startswith("ASK")
            ):
                raise PyRedisError(
                    "Slot moved to often or wrong shard_key, giving up,"
                )
            if errstr.startswith("MOVED"):
                if not shard_key:
                    raise ReplyError(
                        f"Explicitly set socket, but key does "
                        f"not belong to this redis: {sock}"
                    )
                self._map_id = self._map.update(self._map_id)
                self._cleanup_conns()
                return self.execute(
                    *args,
                    shard_key=shard_key,
                    retries=retries - 1
                )
            elif errstr.startswith("ASK"):
                sock = errstr.split()[2].replace(
                    ":",
                    "_"
                )
                return self.execute(
                    *args,
                    sock=sock,
                    retries=retries - 1,
                    asking=True
                )
            else:
                raise err
        except (PyRedisConnError, PyRedisConnReadTimeout) as err:
            self._conns[sock].close()
            del self._conns[sock]
            self._map.update(self._map_id)
            raise err
