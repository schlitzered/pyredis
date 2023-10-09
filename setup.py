from setuptools import setup

setup(
    name='python_redis',
    version='0.4.0',
    description='Redis Client',
    long_description="""
Redis Client implementation for Python 3.

Copyright (c) 2021, Stephan Schultchen.

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
        'crc'
    ],
    install_requires=[
        'crc'
    ],
    keywords=[
        'redis'
    ]
)
