#!/usr/bin/env python

try:
    from setuptools import setup
    from setuptools import find_packages
except ImportError:
    from distutils.core import setup

import quotidian

packages = ['quotidian', 'quotidian.modules', 'quotidian.cli']

modules = ['quotidian.modules.' + p for p in find_packages('quotidian/modules')]

setup(
    name='quotidian',
    version=0.1,
    description='A simple platform for unifying the data in your life.',
    author='Caleb Foust',
    author_email='cfoust@sqweebloid.com',
    packages = packages + modules,
    install_requires=['peewee'],
    entry_points = {
    	'console_scripts': [
    		'quot = quotidian.cli:main'
    	]
    }
)