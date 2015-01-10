import os, importlib

"""Dynamically loads all the modules. This is for various reasons, but mostly
it will make adding new ones more mindless and imports them as objects."""
def initialize():
	# Get the modules directory
	directory = '\\'.join(__file__.split('\\')[:-1])

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

		# Hold up, some modules might be directories.
		if os.path.isdir(directory + '\\' + file):
			ok = True

		if ok:
			filtered.append(file)

	files = filtered
	# strip .py

	filtered = []
	for file in files:
		if '.py' in file:
			filtered.append(file[:-3])
		else:
			filtered.append(file)
	files = filtered
	
	modules = []
	for file in files:
		module = importlib.import_module('quotidian.modules.' + file)

		if not hasattr(module, 'info'):
			raise Exception('Module %s does not have info array.' % file)

		module.info['shortname'] = file
		modules.append(module)

	# Check validity of each module
	validModules = []
	for module in modules:
		info = module.info

		requiredKeys = ['name','description']

		for key in requiredKeys:
			if not key in info:
				raise Exception('Module %s does not have property %s in info array.' % (info['shortname'],key))

		requiredFuncs = ['check','parse']
		for func in requiredFuncs:
			if not hasattr(module,func):
				raise Exception('Module %s does not have required method %s.' % (info['shortname'],func))

		validModules.append(module)

	modules = validModules

	return modules