__author__ = "schlitzer"

"""
Redis Client implementation for Python 3.

Copyright (c) 2015, Stephan Schultchen.

License: MIT (see LICENSE for details)
"""

from pyredis.exceptions import PyRedisConnError
from pyredis.exceptions import PyRedisConnReadTimeout
from pyredis.exceptions import PyRedisConnClosed
from pyredis.exceptions import PyRedisError
from pyredis.exceptions import ProtocolError
from pyredis.exceptions import ReplyError
from pyredis.exceptions import PyRedisURLError
from pyredis.client import Client
from pyredis.client import AsyncClient
from pyredis.client import ClusterClient
from pyredis.client import AsyncClusterClient
from pyredis.client import HashClient
from pyredis.client import AsyncHashClient
from pyredis.client import PubSubClient
from pyredis.client import AsyncPubSubClient
from pyredis.client import SentinelClient
from pyredis.client import AsyncSentinelClient
from pyredis.pool import ClusterPool
from pyredis.pool import AsyncClusterPool
from pyredis.pool import HashPool
from pyredis.pool import AsyncHashPool
from pyredis.pool import Pool
from pyredis.pool import AsyncPool
from pyredis.pool import SentinelHashPool
from pyredis.pool import AsyncSentinelHashPool
from pyredis.pool import SentinelPool
from pyredis.pool import AsyncSentinelPool

__all__ = [
    "get_by_url",
    "Client",
    "AsyncClient",
    "ClusterClient",
    "AsyncClusterClient",
    "ClusterPool",
    "AsyncClusterPool",
    "HashClient",
    "AsyncHashClient",
    "PubSubClient",
    "AsyncPubSubClient",
    "SentinelClient",
    "AsyncSentinelClient",
    "HashPool",
    "AsyncHashPool",
    "Pool",
    "AsyncPool",
    "SentinelPool",
    "AsyncSentinelPool",
    "SentinelHashPool",
    "AsyncSentinelHashPool",
    "PyRedisConnError",
    "PyRedisConnReadTimeout",
    "PyRedisConnClosed",
    "PyRedisError",
    "ProtocolError",
    "ReplyError",
]


def get_by_url(
    url,
    async_client=False
):
    scheme, rest = url.split("://", 1)
    conns = list()
    kwargs = dict()
    if "?" in rest:
        connect, opts = rest.split("?", 1)
    else:
        connect = rest
        opts = None
    for conn in connect.split(","):
        conn = conn.rsplit(":", 1)
        if len(conn) == 2:
            conn[1] = int(conn[1])
        conns.append(conn)
    if opts:
        kwargs = dict()
        for opt in opts.split("&"):
            key, value = opt.split("=", 1)
            kwargs[key] = _opts_type_helper(key, value)
    try:
        if scheme == "cluster":
            if async_client:
                return AsyncClusterPool(seeds=conns, **kwargs)
            return ClusterPool(seeds=conns, **kwargs)
        elif scheme == "redis":
            host = conns[0][0]
            try:
                port = conns[0][1]
            except IndexError:
                port = 6379
            if async_client:
                return AsyncPool(
                    host=host,
                    port=port,
                    **kwargs
                )
            return Pool(
                host=host,
                port=port,
                **kwargs
            )
        elif scheme == "sentinel":
            if "buckets" in kwargs:
                if async_client:
                    return AsyncSentinelHashPool(sentinels=conns, **kwargs)
                return SentinelHashPool(sentinels=conns, **kwargs)
            if async_client:
                return AsyncSentinelPool(sentinels=conns, **kwargs)
            return SentinelPool(sentinels=conns, **kwargs)
        elif scheme == "pubsub":
            host = conns[0][0]
            try:
                port = conns[0][1]
            except IndexError:
                port = 6379
            if async_client:
                return AsyncPubSubClient(
                    host=host,
                    port=port,
                    **kwargs
                )
            return PubSubClient(
                host=host,
                port=port,
                **kwargs
            )
        else:
            raise PyRedisURLError("invalid schema: {0}")
    except TypeError as err:
        raise PyRedisURLError(
            "unexpected or missing options specified: {0}".format(err)
        )


def _opts_type_helper(opt, value):
    if opt in ["database", "pool_size", "retries"]:
        return int(value)
    elif opt in ["conn_timeout", "read_timeout"]:
        return float(value)
    elif opt in ["slave_ok"]:
        if value in ["true", "True", 1]:
            return True
        else:
            return False
    else:
        return value
