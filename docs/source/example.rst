Usage Example
*************

Simple Client Usage
-------------------
.. code:: python

    from pyredis import Client

    client = Client(host="localhost")
    client.ping()


Bulk Mode
---------

Bulk Mode can be used to import large amounts of data in
a short time. With bulk mode enabled sending requests and
fetching results is separated from each other. Which will
save many network round trips, improving query performance.

All executed commands will return None.

There is a threshold, which defaults to 5000 requests,
after which the results of the previous requests are
fetched into a list. If you are not interested in the
results, this can be disabled by calling bulk_start
with the parameter keep_results=False.

Fetching results, when the threshold is reached is a transparent
operation. The client will only notice that the execution
of the the request triggering the threshold will take a little longer.

Calling bulk_stop() will fetch all remaining results, and return a list
with fetched results. This list can also contain exceptions from failed
commands.

.. code:: python

    from pyredis import Client

    client = Client(host="localhost")
    client.bulk_start()
    client.set('key1', 'value1)
    client.set('key1', 'value1)
    client.set('key1', 'value1)
    client.bulk_stop()
    [b'OK', b'OK', b'OK']


Using a Connection Pool
-----------------------
.. code:: python

    from pyredis import Pool

    pool = Pool(host="localhost")
    client = pool.aquire()
    client.ping()
    b'PONG'
    pool.release(client)


Using a Cluster Connection Pool
-------------------------------
.. code:: python

    from pyredis import ClusterPool

    pool = ClusterPool(seeds=[('seed1', 6379), ('seed2', 6379), ('seed3', 6379)])
    client = pool.aquire()
    client.ping(shard_key='test')
    b'PONG'
    pool.release(client)


Using a Sentinel backed Connection Pool
---------------------------------------
.. code:: python

    from pyredis import SentinelPool

    pool = SentinelPool(sentinels=[('sentinel1', 26379), ('sentinel2', 26379), ('sentinel3', 26379)], name=pool_name)
    client = pool.aquire()
    client.ping()
    b'PONG'
    pool.release(client)


Getting Pool by URL
-------------------
.. code:: python

    from pyredis import get_by_url
    pool1 = get_by_url('redis://localhost?password=topsecret')
    pool1 = get_by_url('redis://localhost:6379?db=0&password=topsecret')
    sentinel = get_by_url('sentinel://seed1:6379,seed2,seed3:4711?name=pool_name&db=0&password=topsecret')
    cluster = get_by_url('redis://seed1:6379,seed2:4711,seed3?db=0')


Getting PubSubClient by URL
---------------------------
.. code:: python

    from pyredis import get_by_url
    # it is not save to share this client between threads
    pubsub = get_by_url('pubsub://localhost?password=topsecret')

Publish Subscribe
-----------------
.. code:: python

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

