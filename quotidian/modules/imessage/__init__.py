info = {
	'name': 'Apple iMessage',
	'version': 0.2,
	'description': """Takes in files from an iPhone backup to get information about iMessage data."""
}

import os, json, csv, datetime

from models import *

def check(path):
	# Grab the DB filename
	dbFile = path + '/sms.db'

	# If the db file doesn't exist, return false
	if not os.path.exists(dbFile):
		return False

	# Try to connect to the DB
	sqlitedb = SqliteDatabase(dbFile)
	sqlitedb.connect()

	# See if our models match up
	database.initialize(sqlitedb)
	
	# Sweeet
	return True

# Apple uses Apple Epoch time starting on 1/1/2001
diff = (datetime.datetime(2001,1,1) - datetime.datetime(1970,1,1)).total_seconds()
def appleToEpoch(stamp):
	return int(stamp + diff)

def numToConsistent(num):
	tfm = ''.join([str(s) for s in num if s.isdigit()])
	if len(tfm) == 10:
		tfm = '1' + tfm
	return '+' + tfm

def parse(path):
	# Grab the DB path
	dbFile = path + '/sms.db'

	# Connect to the DB we know exists
	sqlitedb = SqliteDatabase(dbFile)
	sqlitedb.connect()

	# Link up our models
	database.initialize(sqlitedb)

	# Grab the people path
	peopleFile = path + '/people.csv'
	people = []

	# If we have a people csv, iterate over and grab all its data
	if os.path.exists(peopleFile):
		with open(peopleFile) as peoplecsv:
			peoplereader = csv.reader(peoplecsv, delimiter=',', quotechar='"')
			for row in peoplereader:
				people.append(row)

	# The dict of messages (key is message id)
	messages = {}

	# Key-value transform to go from emails and numbers to contact names
	peopleStore = {}

	# Key-value transform to go from handleID to email/number
	handleStore = {}

	# Iterate over all the message joins
	for messageJoin in ChatMessageJoin.select():

		# Holds information about a specific conversation
		chat = messageJoin.chat

		# Holds information about a specific message in the conversation
		message = messageJoin.message

		if message.handle == 0:
			continue

		# Generate the handle store if it isn't there
		if not str(message.handle) in handleStore:
			handleStore[str(message.handle)] = Handle.select().where(Handle.rowid == message.handle).get().id

		# We now have a phone number or email for this
		address = handleStore[str(message.handle)]

		found = False
		person = ''

		# Now let's search through the people if we have one matching this address
		if not address in peopleStore:
			for row in people:
				email = row[-3]

				# Have to transform the phone numbers because they're in all different
				# formats
				home = numToConsistent(row[-4])
				mobile = numToConsistent(row[-5])
				
				name = (row[1] + ' ' + row[2]).strip()

				# If we have a match anywhere, we add it to the store for 
				# future reference
				if email == address or mobile == address or home == address:
					peopleStore[address] = name
					person = name
					found = True
		else:
			# Just grabs it from the store
			person = peopleStore[address]
			found = True

		# if not found:
			# print 'Could not find contact for address %s' % address

		messages[str(message.rowid)] = {
			'contact': person if found else address,
			'timestamp': appleToEpoch(message.date),
			'readTime': appleToEpoch(message.date_read) if message.date_read != 0 else 0,
			'read': message.is_read,
			'text': message.text,
			'isiMessage': message.service == 'iMessage',
			'incoming': not message.is_from_me
		}


	# Now we go through and see if any messages had attachments
	for pair in MessageAttachmentJoin.select():
		# Gets the message this pair refers to
		try:
			message = messages[str(pair.message)]
		except KeyError:
			continue

		# Gets the attachment object
		attachment = pair.attachment

		# The filename of the attachment
		filename = attachment.filename

		oldname = filename

		# Transform the filename into the local path
		filename = filename.replace('~/Library/SMS',path)
		filename = filename.replace('/var/mobile/Library/SMS',path)

		# Add it to the message
		message['attachment'] = filename

	# Transform the messages into their final form
	compiled = []
	for id, message in messages.iteritems():
		compiled.append((datetime.datetime.fromtimestamp(message['timestamp']), message))

	# Do an integrity scan
	remove = []
	for i,item in enumerate(compiled):
		if not item[0]:
			remove.append(i)

	print "%d messages had no date" % len(remove)
	
	return compiled