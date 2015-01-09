#!/usr/bin/env python

import os


class Collection:

	def __init__(self, folder_name, modules):
		self.folder_name = folder_name
		self.modules = modules

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

		