#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
import codecs
import os

try:
    import multiprocessing  # noqa
except ImportError:
    pass

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages  # noqa


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


install_requires = [
    'requests>=0.13.1',
]

tests_require = [
    'nose>=1.1.2',
]

setup(
    name="korta",
    version="0.1.4.2",
    packages=find_packages(),
    install_requires=install_requires,
    package_data={
        'korta': ['certs/*.pem'],
    },
    tests_require=tests_require,
    extras_require={'test': tests_require},
    test_suite='nose.collector',
    author="Stefan Kjartansson",
    author_email="esteban.supreme@gmail.com",
    description="Korta Client library",
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
)
