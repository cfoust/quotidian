#!/usr/bin/env python

import os, datetime, sys, traceback
import drury


class Collection:

	def __init__(self, folder_name, modules):
		self.folder_name = folder_name

		# Create folder if it doesn't exist
		if not os.path.isdir(folder_name):
			print "Folder %s was not found, so it was created." % folder_name
			os.makedirs(folder_name)

		# Create (or update) guide to usable modules
		with open(folder_name + 'modules-readme.txt','w') as f:
			print "%d installed modules." % len(modules)

			# Add the header
			template = '\\'.join(__file__.split('\\')[:-1]) + '\\guide-template.txt'
			with open(template,'r') as t:
				f.write(t.read())

			f.write('\n\n')

			for module in modules:
				title = '# %s \n# Folder Name: %s' % (module.info['name'], 
													module.info['shortname'])

				f.write(title + '\n')
				f.write('='.join(['' for x in range(len(title))]) + '\n')
				f.write(module.info['description'])
				f.write('\n\n')

		moduleDict = {}
		for module in modules:
			moduleDict[module.info['shortname']] = module

		self.modules = moduleDict
		self.db = drury.Drury(folder_name + 'baked.db')

	def hasData(self, module_name):
		if not module_name in self.modules:
			raise Exception('No such module: %s' % module_name)

		if not os.path.isdir(self.folder_name + module_name):
			return False

		try:
			return self.modules[module_name].check(self.folder_name + module_name)
		except:
			print 'There was an exception when checking for module %s:' % module_name
			print traceback.format_exc()
			return False

	def bakeData(self, module_name):
		if not module_name in self.modules:
			raise Exception('No such module: %s' % module_name)

		if not os.path.isdir(self.folder_name + module_name):
			raise Exception('No data found for module %s' % module_name)

		data = self.modules[module_name].parse(self.folder_name + module_name)
		self.db.bakeData(module_name,data)

	# Need to be internal classes, not used elsewhere
	class Range:
		def __init__(self,collection):
			self.collection = collection

		def all(self):
			self.start = datetime.datetime.min
			self.end = datetime.datetime.max

		def between(self,start,end):
			# todo: sanity check these values some more

			if not end > start:
				raise Exception('Invalid range, end is before start.')

			self.start = start
			self.end = end

	class Selection:
		def __init__(self,forRange):
			self.range = forRange