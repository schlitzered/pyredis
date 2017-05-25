Introduction
************
Redis Client implementation for Python. The Client only supports Python 3 for the moment.
If there is enough interest, i will make it work with Python 2.

Currently implemented Features:
  - Base Redis Client
  - Publish Subscribe Client
  - Sentinel Client
  - Connection Pool
  - Sentinel Backed Connection Pool
  - Client & Pool for Redis Cluster
  - Bulk Mode ( Not supported with Redis Cluster )
  - Client & Pool with Static Hash Cluster (Supports Bulk Mode)
  - Sentinel Backed Pool with Static Hash Cluster (Supports Bulk Mode)

Documentation
-------------

http://pyredis.readthedocs.org/


Installing
----------

pyredis can be installed via pip as follows:

.. code::

    pip install python_redis

Author
------

Stephan Schultchen <stephan.schultchen@gmail.com>

License
-------

Unless stated otherwise on-file pyredis uses the MIT license,
check LICENSE file.

Contributing
------------

If you'd like to contribute, fork the project, make a patch and send a pull
request.


