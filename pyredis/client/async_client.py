from pyredis import commands
from pyredis.connection import AsyncConnection


class AsyncClient(
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
    def __init__(self, **kwargs):
        super().__init__()
        self._conn = AsyncConnection(**kwargs)

    async def execute(self, *args):
        await self._conn.write(*args)
        return await self._conn.read()

    async def close(self):
        await self._conn.close()

    @property
    def closed(self):
        return self._conn.closed
