# pyredis

Redis Client implementation for Python 3.

## Features
- Complete Synchronous and Asynchronous (asyncio) counterparts for all client and pool classes.
- Base Redis Client & AsyncClient
- Publish Subscribe Client & AsyncPubSubClient
- Sentinel Client & AsyncSentinelClient
- Connection Pool & AsyncPool
- Sentinel Backed Connection Pool & AsyncSentinelPool
- Client & Pool for Redis Cluster & AsyncClusterPool
- Bulk Mode (Sync & Async, not supported with Redis Cluster)
- Client & Pool with Static Hash Cluster & AsyncHashPool
- Sentinel Backed Pool with Static Hash Cluster & AsyncSentinelHashPool

## Documentation
Documentation can be found on GitHub Pages:
https://schlitzered.github.io/pyredis/

## Installation
`pyredis` can be installed via pip:

```bash
pip install python_redis
```

## Author
Stephan Schultchen <stephan.schultchen@gmail.com>

## License
Unless stated otherwise, `pyredis` uses the MIT license (see the LICENSE file).

## Contributing
If you'd like to contribute, fork the project, make a patch, and send a pull request.
