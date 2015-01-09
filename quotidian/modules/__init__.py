import os, importlib

"""Takes in the path to where the modules are stored. This is so you can 
install it anywhere."""
def initialize(path):
	# Get the modules directory
	directory = '\\'.join(path.split('\\')[:-1])

	files = os.listdir(directory)

	# Clean out anything we don't need
	banned = ['__init__','.pyc','all.py']

	filtered = []
	for file in files:
		ok = True
		for ban in banned:
			if ban in file:
				ok = False

		if not '.py' in file:
			ok = False

		if ok:
			filtered.append(file)

	files = filtered

	# strip .py
	files = [file[:-3] for file in files]
	
	modules = []
	for file in files:
		modules.append(importlib.import_module('quotidian.modules.' + file))
		modules[-1].info['shortname'] = file

	return modules