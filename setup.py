#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


setup(
    name = "korta",
    version = "0.1",
    packages = find_packages(),
    install_requires = [
        'pycurl',
    ],
    package_data = {
        'korta': ['certs/*.pem', 'certs/*.crt'],
    },
    author="Stefan Kjartansson",
    author_email="esteban.supreme@gmail.com",
    description="Korta Client library",
    long_description=open('README.rst').read(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
)
