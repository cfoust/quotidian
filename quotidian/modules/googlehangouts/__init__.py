info = {
	'name': 'Google Hangouts',
	'version': 1.0,
	'description': """Similar to the Google Voice importer, but works on the
Hangouts data exported by Google Takeout. The folder structure should be the
same, that being, googlehangouts/Takeout/Hangouts/. """
}

import os, json
from helpers import HangoutsData

def check(path):
	jsonfile = path + '/Takeout/Hangouts/Hangouts.json'

	if not os.path.exists(jsonfile):
		return False

	with open(jsonfile,'r') as f:
		data = json.loads(f.read())
		if 'conversation_state' in data:
			return True

	return False

def parse(path):
	jsonfile = path + '/Takeout/Hangouts/Hangouts.json'

	messages = []

	with open(jsonfile,'r') as f:
		data = json.loads(f.read())

	# Some classes to make

	reader = HangoutsData(data)

	[c.participants() for c in reader.conversations()] # Have to do this to register all the names

	for conversation in reader.conversations():
		participants = conversation.participants()

		valid = True
		for participant in participants:
			if not participant.getName():
				valid = False

		if valid == False:
			continue


		for message in conversation.messages():
			if message.type() == 'chat_message':
				timeStamp = message.date()
				name = message.sender.getName()
				names = [parti.getName() for parti in participants]
				prototype = {
					'sender': name,
					'recipients': [p for p in names if p != name],
					'text': message.text()
				}
				messages.append((timeStamp,prototype))

	return messages