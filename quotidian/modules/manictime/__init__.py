info = {
	'name': 'Manic Time',
	'version': 1.0,
	'description': """Interprets data from ManicTime, an application that tracks
computer usage over time. 

To use, open up the application and click the \"Tools and settings button\" in
the upper right corner. Click on \"Export\" and select your desired range. Each
\"Timeline\" option has a specific name it has to have in quotidian's folder.

Tags: Not supported.
Computer Usage: computerusage.csv
Applications: applications.csv
Documents: documents.csv

Export your data with these required names."""
}

import os, csv, datetime
import dateutil.parser

def check(path):

	def checkForFile(name,dataName):
		if os.path.exists(path + '/%s.csv' % name):
			with open(path + '/%s.csv' % name, 'rb') as f:
				reader = csv.reader(f, delimiter=',', quotechar='"')
				header = reader.next()
				if header[-1] == dataName:
					return True
		return False

	if checkForFile('documents','Domain'): return True
	if checkForFile('applications','Process'): return True
	if checkForFile('computerusage','Duration'): return True

	return False

def parse(path):
	events = []

	def grabData(name):
		if os.path.exists(path + '/%s.csv' % name):
			with open(path + '/%s.csv' % name, 'rb') as f:
				reader = csv.reader(f, delimiter=',', quotechar='"')

				rows = []
				for row in reader: rows.append(row)

				header = rows[0][-1]
				# Cut out the header
				rows = rows[1:]

				for row in rows:
					manicName = row[0]
					timeStamp = dateutil.parser.parse(row[1])

					durationParts = [int(x) for x in row[3].split(':')]
					seconds = 0
					seconds += durationParts[0]*3600
					seconds += durationParts[1]*60
					seconds += durationParts[2]
					data = {
						'type': name,
						'name': manicName,
						'duration': seconds
					}
					if len(row) > 4:
						data[header.lower()] = row[-1]

					events.append((timeStamp,data))


	grabData('documents')
	grabData('applications')
	grabData('computerusage')

	return events