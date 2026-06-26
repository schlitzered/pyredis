from pyredis import commands
import pyredis.client
from pyredis.exceptions import PyRedisError


class Client(
    commands.Connection,
    commands.Geo,
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
    """Base Client for Talking to Redis."""

    def __init__(self, **kwargs):
        super().__init__()
        self._conn = pyredis.client.Connection(**kwargs)
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
        return self._bulk

    def bulk_start(self, bulk_size=5000, keep_results=True):
        if self.bulk:
            raise PyRedisError("Already in bulk mode")
        self._bulk = True
        self._bulk_size = bulk_size
        self._bulk_size_current = 0
        if keep_results:
            self._bulk_results = []
            self._bulk_keep = True

    def bulk_stop(self):
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
        self._conn.close()

    @property
    def closed(self):
        return self._conn.closed

    def execute(self, *args):
        if not self._bulk:
            return self._execute_basic(*args)
        else:
            self._execute_bulk(*args)
