info = {
	'name': 'Facebook',
	'version': 1.0,
	'description': """Parses the data from Facebook's account export feature.
The data can be found by going into your settings and clicking the \"Download
a copy of your Facebook data\" link and following the instructions. Unzip the 
folder they send to you here. Folder structure should be 
facebook/facebook-username.""",
	'dependencies': ['bs4','dateutil']
}

import os, datetime

from bs4 import BeautifulSoup as soup
import dateutil.parser

def check(path):
	for file in os.listdir(path):
		if 'facebook-' in file:
			direcPath = path + '/' + file + '/'

			if not os.path.exists(direcPath + 'html'):
				continue
			
			if not os.path.exists(direcPath + 'html/messages.htm'):
				continue

			if not os.path.exists(direcPath + 'html/wall.htm'):
				continue

			return True

	return False

def parse(path):

	direcPath = ""
	for file in os.listdir(path):
		if 'facebook-' in file:
			direcPath = path + '/' + file + '/'
			break

	htmlDir = direcPath + 'html/'

	events = []

	unknownParticipants = {}

	with open(htmlDir + 'messages.htm','r') as f:
		bs = soup(f.read())
		threads = bs.findAll(attrs={'class': 'thread'})
		for thread in threads:
			participants = thread.contents[0].split(', ')

			""" The following tries to bruteforce finding the names of people
			for whom Facebook did not provide any information. It worked, but 
			took a very long time, something like 300 seconds for me, and really
			wasn't worth the time. It found only maybe 30% of people, so not 
			super useful. I'll leave it here for if we ever want to reinclude it.

			Normal build times without the code: 10s
			With it: 300s

			Not worth it."""
			# fixedParticipants = []
			# for participant in participants:
			# 	if '@facebook.com' in participant:
			# 		# Try to grab the name from FB
			# 		number = participant[:-13]
			# 		if number in unknownParticipants:
			# 			participant = unknownParticipants[number]
			# 		else:
			# 			try:
			# 				r = requests.get('http://facebook.com/' + number)
			# 				title = soup(r.text).title.string

			# 				if 'Not Found' in title or 'Unavailable' in title:
			# 					# Likely deleted or hidden profile
			# 					fixedParticipants.append(participant)
			# 					continue
			# 				else:
			# 					# Found a name successfully
			# 					name = title.split(' | ')[0]
			# 					unknownParticipants[number] = name
			# 					fixedParticipants.append(name)
			# 			except:
			# 				# Something went wrong, just use the email
			# 				fixedParticipants.append(participant)
			# 				continue
			# 	else:
			# 		fixedParticipants.append(participant)
			# participants = fixedParticipants

			messages = thread.findAll(attrs={'class': 'message'})
			messageText = thread.findAll('p')
			for index, message in enumerate(messages):
				header = message.find(attrs={'class': 'message_header'})
				user = header.find(attrs={'class': 'user'}).string

				timestamp = header.find(attrs={'class': 'meta'}).string
				timestamp = dateutil.parser.parse(timestamp)

				text = messageText[index].string
				prototype = {
					'type': 'message',
					'sender': user,
					'recipients': [p for p in participants if p != user],
					'text': text
				}
				events.append((timestamp,prototype))

	with open(htmlDir + 'wall.htm','r') as f:
		bs = soup(f.read())
		c = bs.find(attrs={'class': 'contents'}).find('div')
		if c:
			for item in c.children:
				if item.find(attrs={'class': 'meta'}):
					timestamp = item.find(attrs={'class': 'meta'}).string
					timestamp = dateutil.parser.parse(timestamp)

					event = item.contents[1]

					comment = item.find(attrs={'class': 'comment'})
					if comment:
						comment = comment.string

					"""I sort of ran out of steam here on working on this, 
					because it's ultimately not that high priority and it's 
					gonna be pretty tedious to come up with some regexes to get
					data from all the different events. But it's doable, for 
					whoever's interested in getting this kind of data. Messages 
					were my priority for social graph kind of stuff, because
					Facebook does not provide very much about the Wall events."""

	return events