# Usage Example

## Simple Client Usage

```python
from pyredis import Client

client = Client(host="localhost")
client.ping()
```

## Bulk Mode

Bulk Mode can be used to import large amounts of data in a short time. With bulk mode enabled sending requests and fetching results is separated from each other. Which will save many network round trips, improving query performance.

All executed commands will return None.

There is a threshold, which defaults to 5000 requests, after which the results of the previous requests are fetched into a list. If you are not interested in the results, this can be disabled by calling `bulk_start` with the parameter `keep_results=False`.

Fetching results, when the threshold is reached is a transparent operation. The client will only notice that the execution of the request triggering the threshold will take a little longer.

Calling `bulk_stop()` will fetch all remaining results, and return a list with fetched results. This list can also contain exceptions from failed commands.

```python
from pyredis import Client

client = Client(host="localhost")
client.bulk_start()
client.set('key1', 'value1')
client.set('key2', 'value2')
client.set('key3', 'value3')
client.bulk_stop()
[b'OK', b'OK', b'OK']


from pyredis import HashClient

client = Client(buckets=[('host1', 6379), ('host2', 6379), ('host3', 6379)])
client.bulk_start()
client.set('key1', 'value1')
client.set('key2', 'value2')
client.set('key3', 'value3')
client.bulk_stop()
[b'OK', b'OK', b'OK']
```

## Using a Connection Pool

```python
from pyredis import Pool

pool = Pool(host="localhost")
client = pool.acquire()
client.ping()
b'PONG'
pool.release(client)
```

## Using a Cluster Connection Pool

```python
from pyredis import ClusterPool

pool = ClusterPool(seeds=[('seed1', 6379), ('seed2', 6379), ('seed3', 6379)])
client = pool.acquire()
client.ping(shard_key='test')
b'PONG'
pool.release(client)
```

## Using a Hash Connection Pool

```python
from pyredis import HashPool

pool = HashPool(buckets=[('host1', 6379), ('host2', 6379), ('host3', 6379)])
client = pool.acquire()
client.ping(shard_key='test')
b'PONG'
pool.release(client)
```

## Using a Sentinel backed Connection Hash Pool

```python
from pyredis import SentinelHashPool

pool = SentinelHashPool(sentinels=[('sentinel1', 26379), ('sentinel2', 26379), ('sentinel3', 26379)], buckets=['bucket1', 'bucket2', 'bucket3'])
client = pool.acquire()
client.ping(shard_key='test')
b'PONG'
pool.release(client)
```

## Using a Sentinel backed Connection Pool

```python
from pyredis import SentinelPool

pool = SentinelPool(sentinels=[('sentinel1', 26379), ('sentinel2', 26379), ('sentinel3', 26379)], name=pool_name)
client = pool.acquire()
client.ping()
b'PONG'
pool.release(client)
```

## Getting Pool by URL

```python
from pyredis import get_by_url
pool1 = get_by_url('redis://localhost?password=topsecret')
pool1 = get_by_url('redis://localhost:6379?db=0&password=topsecret')
sentinel = get_by_url('sentinel://seed1:6379,seed2,seed3:4711?name=pool_name&db=0&password=topsecret')
cluster = get_by_url('redis://seed1:6379,seed2:4711,seed3?db=0')
```

## Getting PubSubClient by URL

```python
from pyredis import get_by_url
# it is not save to share this client between threads
pubsub = get_by_url('pubsub://localhost?password=topsecret')
```

## Publish Subscribe

```python
from pyredis import Client, PubSubClient

client = Client(host='localhost')
subscribe = PubSubClient(host='localhost')

subscribe.subscribe('/blub')
subscribe.get()
[b'subscribe', b'/blub', 1]

client.publish('/blub', 'test')
1

subscribe.get()
[b'message', b'/blub', b'test']
```

## Asynchronous Client and Pool Usage

### Simple Async Client Usage

```python
import asyncio
from pyredis import AsyncClient

async def main():
    client = AsyncClient(host="localhost")
    await client.ping()
    await client.close()

asyncio.run(main())
```

### Async Bulk Mode

```python
import asyncio
from pyredis import AsyncClient

async def main():
    client = AsyncClient(host="localhost")
    await client.bulk_start()
    await client.set("key1", "value1")
    await client.set("key2", "value2")
    await client.set("key3", "value3")
    results = await client.bulk_stop()
    print(results)
    await client.close()

asyncio.run(main())
```

### Using an Async Connection Pool

```python
import asyncio
from pyredis import AsyncPool

async def main():
    pool = AsyncPool(host="localhost")
    client = await pool.acquire()
    await client.ping()
    await pool.release(client)

asyncio.run(main())
```

### Using an Async Cluster Connection Pool

```python
import asyncio
from pyredis import AsyncClusterPool

async def main():
    pool = AsyncClusterPool(
        seeds=[
            ("seed1", 6379),
            ("seed2", 6379)
        ]
    )
    client = await pool.acquire()
    await client.ping(shard_key="test")
    await pool.release(client)

asyncio.run(main())
```

### Using an Async Hash Connection Pool

```python
import asyncio
from pyredis import AsyncHashPool

async def main():
    pool = AsyncHashPool(
        buckets=[
            ("host1", 6379),
            ("host2", 6379)
        ]
    )
    client = await pool.acquire()
    await client.ping(shard_key="test")
    await pool.release(client)

asyncio.run(main())
```

### Using an Async Sentinel backed Connection Pool

```python
import asyncio
from pyredis import AsyncSentinelPool

async def main():
    pool = AsyncSentinelPool(
        sentinels=[
            ("sentinel1", 26379),
            ("sentinel2", 26379)
        ],
        name="mymaster"
    )
    client = await pool.acquire()
    await client.ping()
    await pool.release(client)

asyncio.run(main())
```

### Getting Async Pools/Clients by URL

```python
from pyredis import get_by_url

pool = get_by_url(
    url="redis://localhost?password=topsecret",
    async_client=True
)

pubsub = get_by_url(
    url="pubsub://localhost?password=topsecret",
    async_client=True
)
```

### Async Publish Subscribe

```python
import asyncio
from pyredis import AsyncClient
from pyredis import AsyncPubSubClient

async def main():
    client = AsyncClient(host="localhost")
    subscribe = AsyncPubSubClient(host="localhost")

    await subscribe.subscribe("/blub")
    res1 = await subscribe.get()
    print(res1)

    await client.publish(
        "/blub",
        "test"
    )
    res2 = await subscribe.get()
    print(res2)

    await client.close()
    await subscribe.close()

asyncio.run(main())
```

