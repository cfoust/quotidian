#!/usr/bin/env python

# Grab our module list
import modules as parsers

modules = parsers.initialize()

from quotidian import Collection as _collection

def load(foldername):
	# Injects the modules into a new collection and returns it
	return _collection(foldername,modules)
