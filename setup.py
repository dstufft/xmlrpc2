#!/usr/bin/env python
from setuptools import setup, find_packages

install_requires = [
]

setup(
    name="xmlrpc2",
    version="0.1dev",

    description="",
    #long_description=open("README.rst").read(),
    url="https://github.com/dstufft/xmlrpc2",
    #license=open("LICENSE").read(),

    author="Donald Stufft",
    author_email="donald.stufft@gmail.com",

    install_requires=install_requires,

    extras_require={},

    packages=find_packages(exclude=["tests"]),
    zip_safe=False,
)
