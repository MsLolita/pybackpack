#!/usr/bin/env python
from setuptools import setup

setup(
    name='pybackpack',
    version='0.0.1',
    packages=['backpack'],
    description='Backpack REST API python implementation',
    long_description_content_type="text/x-rst",
    url='https://github.com/MsLolita/pybackpack',
    author='Web3 Enjoyer',
    license='MIT',
    author_email='',
    install_requires=[
        'aiohttp', 'ed25519', 'PyNaCl'
    ],
    keywords='backpack solana.py exchange rest api bitcoin ethereum btc eth sol solana',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
