#!/usr/bin/env python
from setuptools import setup, find_packages

install_requires = [
    "requests",
]

setup(
    name="xmlrpc2",
    version="0.1dev",

    description="A port of xmlrpc from Python3 to Python 2.x using the Requests library",
    long_description=open("README.rst").read(),
    url="https://github.com/dstufft/xmlrpc2",
    license=open("LICENSE").read(),

    author="Donald Stufft",
    author_email="donald.stufft@gmail.com",

    install_requires=install_requires,

    extras_require={
        "pytz": ["pytz"],
        "lxml": ["lxml"],
    },

    packages=find_packages(exclude=["tests"]),
    zip_safe=False,
)
