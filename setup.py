from setuptools import setup

import pyredis

setup(
    name='python_redis',
    version='0.0.3',
    description='Redis Client',
    long_description=pyredis.__doc__,
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
    install_requires=[
        'crc16'
    ],
    keywords=[
        'redis'
    ]
)
