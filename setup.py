from setuptools import setup

setup(
    name='python_redis',
    version='0.1.7',
    description='Redis Client',
    long_description="""
Redis Client implementation for Python 3.

Copyright (c) 2016, Stephan Schultchen.

License: MIT (see LICENSE for details)
    """,
    packages=['pyredis'],
    url='https://github.com/schlitzered/pyredis',
    license='MIT',
    author='schlitzer',
    author_email='stephan.schultchen@gmail.com',
    test_suite='test',
    platforms='posix',
    classifiers=[
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3'
    ],
    setup_requires=[
        'crc16'
    ],
    install_requires=[
        'crc16'
    ],
    keywords=[
        'redis'
    ]
)
