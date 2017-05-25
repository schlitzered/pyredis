__author__ = 'schlitzer'

"""
Redis Client implementation for Python 3.

Copyright (c) 2015, Stephan Schultchen.

License: MIT (see LICENSE for details)
"""

from pyredis.exceptions import *
from pyredis.client import Client, ClusterClient, HashClient, PubSubClient, SentinelClient
from pyredis.pool import ClusterPool, HashPool, Pool, SentinelHashPool, SentinelPool

__all__ = [
    'get_by_url',
    'Client',
    'ClusterClient',
    'ClusterPool',
    'HashClient',
    'PubSubClient',
    'SentinelClient',
    'HashPool',
    'Pool',
    'SentinelPool',
    'SentinelHashPool',
    'PyRedisConnError',
    'PyRedisConnReadTimeout',
    'PyRedisConnClosed',
    'PyRedisError',
    'ProtocolError',
    'ReplyError'
]


def get_by_url(url):
    scheme, rest = url.split('://', 1)
    conns = list()
    kwargs = dict()
    if '?' in rest:
        connect, opts = (rest.split('?', 1))
    else:
        connect = rest
        opts = None
    for conn in connect.split(","):
        conn = conn.rsplit(':', 1)
        if len(conn) == 2:
            conn[1] = int(conn[1])
        conns.append(conn)
    if opts:
        kwargs = dict()
        for opt in opts.split('&'):
            key, value = opt.split('=', 1)
            kwargs[key] = _opts_type_helper(key, value)
    try:
        if scheme == "cluster":
            return ClusterPool(seeds=conns, **kwargs)
        elif scheme == "redis":
            host = conns[0][0]
            try:
                port = conns[0][1]
            except IndexError:
                port = 6379
            return Pool(host=host, port=port, **kwargs)
        elif scheme == "sentinel":
            return SentinelPool(sentinels=conns, **kwargs)
        elif scheme == "pubsub":
            host = conns[0][0]
            try:
                port = conns[0][1]
            except IndexError:
                port = 6379
            return PubSubClient(host=host, port=port, **kwargs)
        else:
            raise PyRedisURLError("invalid schema: {0}")
    except TypeError as err:
        raise PyRedisURLError("unexpected or missing options specified: {0}".format(err))


def _opts_type_helper(opt, value):
    if opt in ['database', 'pool_size', 'retries']:
        return int(value)
    elif opt in ['conn_timeout', 'read_timeout']:
        return float(value)
    elif opt in ['slave_ok']:
        if value in ['true', 'True', 1]:
            return True
        else:
            return False
    else:
        return value
