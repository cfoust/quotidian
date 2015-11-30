info = {
	'name': 'Google Voice',
	'version': 1.0,
	'description': """Parses the data from Google Takeout for Google Voice. 
Gives details about calls, text messages, and, when possible, voicemails.

Download an archive of your Google Voice data from the following webpage to 
get your data: https://www.google.com/settings/takeout. Unzip and put the
Takout folder found in the archive into this module's folder.

The folder structure should look like googlevoice/Takeout/Google Voice.""",
	'dependencies': ['bs4','dateutil']
}

from peewee import *
import os, datetime, traceback

from bs4 import BeautifulSoup as soup
import dateutil.parser

def check(path):
	voice = path + '/Takeout/Voice/Calls/'

	if not os.path.exists(voice):
		return False

	return True

def parse(path):
	voice = path + '/Takeout/Voice/Calls/'
	files = []

	for subdir, dirs, filez in os.walk(voice):
	    for file in filez:
	    	if '- Text -' in file:
				ftable = {}
				ftable['name'] = file
				try:
					f=open(voice + file, 'r')
				except:
					continue
				ftable['contents'] = f.read()
				files.append(ftable)

	info = []
	
	for file in files:
		parts = file['name'].split(' - ')
		contact = parts[0]

		# To deal with the Windows file system encoding
		try:
			contact = contact.decode('latin-1')
		except:
			pass

		s = soup(file['contents'],'html.parser')

		messages = s.findAll(attrs={'class': 'message'})
		for message in messages:
			timestamp = message.findAll('abbr')[0]['title']
			
			timestamp = dateutil.parser.parse(timestamp)
			timestamp = datetime.datetime(timestamp.year,timestamp.month,timestamp.day,timestamp.hour,timestamp.minute,timestamp.second)

			contactname = message.findAll('cite')[0].findAll(attrs={'class': 'fn'})[0].text

			messagetext = message.findAll('q')[0].text

			
			text = {
				'type': 'text',
				'contact': contact,
				'incoming': contactname == contact,
				'text': messagetext
			}



			info.append((timestamp,text))

	return info