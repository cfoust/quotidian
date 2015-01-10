import os, datetime
from loader import *

info = {
	'name': 'Momento',
	'version': 1.0,
	'description': """Hooks into the data provided by Momento's
(http://momentoapp.com/) \"Export to Text Files\" function. To use,
export one file for each day (it's an option in the menu) and dump the contents
of the zip that it gives you to this module's folder. You should have an Attachments 
folder and all of the entries."""
}

"""Checks to see if the folder specified by path has proper Momento data in it.
Returns true or false."""
def check(path):
	files = os.listdir(path)

	for file in files:

		# See if we can parse it
		try:
			Day.fromFile(path + '\\' + file)
			return True
		except:
			continue
	return False


"""Gets all the data. Returns it as a tuple of (datetime.datetime,dictionary)
for each data point."""
def parse(path):
	files = os.listdir(path)

	days = []
	for file in files:
		try:
			days.append(Day.fromFile(path + '\\' + file))
		except:
			continue

	entries = []
	for day in days:
		dayTime = day.date
		for entry in day.entries:
			entryTime = entry['time']
			timeStamp = datetime.datetime(dayTime.year,
										  dayTime.month,
										  dayTime.day,
										  entryTime.hour,
										  entryTime.minute,
										  entryTime.second)
			del entry['time']
			entries.append((timeStamp,entry))

	return entries