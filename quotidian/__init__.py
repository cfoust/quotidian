#!/usr/bin/env python

# Grab our module list
import modules as parsers

modules = parsers.initialize(modules.__file__)

from quotidian import Collection as _collection

def load(foldername):
	# Injects the modules into a new collection and returns it
	return _collection(foldername,modules)
