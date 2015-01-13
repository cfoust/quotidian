#!/usr/bin/env python

import sys, cliutils, quotidian, os

import modules as parsers
modules = parsers.initialize()

from quotidian import Collection

def main():
	# result = cliutils.argsToRange(sys.argv)
	# start = result[0]
	# end = result[1]
	# rest = result[2]

	args = sys.argv[1:] # Cuts out the script name

	if not len(args) > 0:
		print 'Please provide some arguments.'
		exit()

	command = args[0]
	if command == 'init':
		coll = Collection('quot/',modules)

		print 'Initializing Quotidian to folder "quot/".'
		print 'Please read the contents of quot/modules-readme.txt for details.'
	elif command == 'status':
		def err():
			print 'Error: no quotidian instance initialized.'
			print 'Please type "quot init" to begin.'
			exit()

		if not os.path.exists('quot'):
			err()

		if not os.path.exists('quot/modules-readme.txt'):
			err()
		
	elif command == 'range':
		if not len(args) > 2:
			print 'Not enough arguments to execute range.'
			exit()