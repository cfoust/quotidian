#!/usr/bin/env python

import sys, utils, quotidian, os, datetime

import quotidian

def ensureCollection():
	def err():
		print 'Error: no quotidian instance initialized.'
		print 'Please type "quot init" to begin.'
		exit()

	if not os.path.exists('quot'):
		err()

	if not os.path.exists('quot/modules-readme.txt'):
		err()

def statusTable(data,filler):
	# (name,lastBaked,hasRawData,hasDBData)

	size = [20,48,6,6]

	s = ""
	for i,d in enumerate(data):
		s += d + filler.join(['' for x in range(size[i]-len(d))])
	
	return s


def main():

	args = sys.argv[1:] # Cuts out the script name

	if not len(args) > 0:
		print 'Please provide some arguments.'
		exit()

	command = args[0]
	if command == 'init':
		coll = quotidian.load('quot/')

		print 'Initializing Quotidian to folder "quot/".'
		print 'Please read the contents of quot/modules-readme.txt for details.'
		
	elif command == 'status':
		ensureCollection()
		coll = quotidian.load('quot/')

		print statusTable(('Module Name','Last Baked','Raw?','DB?'),' ')
		print statusTable(['' for x in range(4)],'=')

		for module in coll.getModuleList():
			db = coll.hasDBData(module)
			raw = coll.hasRawData(module)

			if db or raw:
				db = str(db)
				raw = str(raw)
				bd = str(coll.lastBakeTime(module))
				print statusTable((module,bd,raw,db),' ')

	elif command == 'range':
		ensureCollection()
		if not len(args) > 2:
			print 'Not enough arguments to execute range.'
			exit()

	elif command == 'bake':
		ensureCollection()
		coll = quotidian.load('quot/')
		if not len(args) > 1:
			print """Not enough arguments to execute bake. Please list one or more modules."""
			exit()

		modules = coll.getModuleList()

		if 'all' in args:
			choices = modules
		else:
			choices = args[1:]

		for module in choices:
			if module in modules:
				if coll.hasRawData(module):
					print "Baking data for module %s." % module

					startTime = datetime.datetime.now()

					coll.bakeData(module)

					diff = datetime.datetime.now() - startTime

					print 'Bake for module %s completed in %.2fs.' % (module,diff.microseconds / 100000.0)
				else:
					print "No data to bake for module %s." % module