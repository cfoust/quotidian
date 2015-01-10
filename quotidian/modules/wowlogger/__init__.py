info = {
	'name': 'World of Warcraft Logger Addon',
	'version': 1.0,
	'description': """Parses data provided by the LoggerPro AddOn for World
of Warcraft. (http://www.wowinterface.com/downloads/info21335-LoggerPro.html)

To use, get the Logger.lua file from your WTF/Acccount/ACCOUNTNAME/SavedVariables
folder and place it in the proper location."""
}

from slpp import slpp as lua
import os, datetime, traceback

def check(path):
	logfile = path + '/Logger.lua'
	if not os.path.exists(logfile):
		return False

	data = None
	with open(logfile,'r') as f:
		try:
			data = lua.decode(f.read()[9:])
		except:
			return False

	return True

def parse(path):
	logfile = path + '/Logger.lua'

	data = None
	with open(logfile,'r') as f:
		data = lua.decode(f.read()[9:])

	compiled = []
	for day in data:
		try:
			dateStamp = datetime.datetime.strptime(day['date'],"%m/%d/%y")
			summary = {'type': 'summary', 'played': day['tt']}
			compiled.append((dateStamp,summary))
		except:
			continue

		log = []

		# Try to parse the activity log
		# Gets whatever data we can, some is junk

		i = 0
		while True:
			if i in day:
				log.append(day[i])
				i += 1
			else:
				break

		for event in log:
			parts = event.split(' ')
			timeParts = ' '.join(parts[:3])
			rest = ' '.join(parts[3:])
			try:
				timeStamp = datetime.datetime.strptime(timeParts,"%m/%d/%y %I:%M:%S (%p)")
				dict = {'type': 'event',
						'text': rest}
				compiled.append((timeStamp,dict))
			except:
				continue

	return compiled