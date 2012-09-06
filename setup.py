#!/usr/bin/env python
from setuptools import setup, find_packages

install_requires = [
    "lxml",
    "python-dateutil>=2.1",
    "requests",
    "six",
]

setup(
    name="xmlrpc2",
    version="0.2.2",

    description="",
    long_description=open("README.rst").read(),
    url="https://github.com/dstufft/xmlrpc2",
    license=open("LICENSE").read(),

    author="Donald Stufft",
    author_email="donald.stufft@gmail.com",

    install_requires=install_requires,

    extras_require={
        "tests": ["pytest"],
    },

    packages=find_packages(exclude=["tests"]),
    package_data={"": ["LICENSE"]},
    zip_safe=False,
)
