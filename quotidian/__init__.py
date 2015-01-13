#!/usr/bin/env python

# Grab our module list
try:
	import modules as parsers
except ImportError:
	import quotidian.modules as parsers

modules = parsers.initialize()

from quotidian import Collection

def load(foldername):
	# Injects the modules into a new collection and returns it
	return _collection(foldername,modules)
