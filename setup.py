#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import quotidian

packages = ['quotidian']

setup(
    name='quotidian',
    version=0.1,
    description='A simple platform for unifying the data in your life.',
    author='Caleb Foust',
    author_email='cfoust@sqweebloid.com',
    packages=packages,
    install_requires=['peewee']
)