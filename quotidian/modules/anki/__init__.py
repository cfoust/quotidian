info = {
	'name': 'Anki Review Log',
	'version': 1.0,
	'description': """Parses review data from the Anki (http://ankisrs.net/)
spaced repetition system. To use, place your collection.anki2 file in the folder.

The collection.anki2 file is typically found at Documents/Anki/YOURNAME/. """
}

from schema import *
import os, datetime

def check(path):
	dbfile = path + '/collection.anki2'

	if not os.path.exists(dbfile):
		return False

	db = SqliteDatabase(dbfile,**{})
	db.connect()
	dbproxy.initialize(db)

	try:
		Revlog.get()
	except:
		return False

	return True

def parse(path):
	dbfile = path + '/collection.anki2'

	db = SqliteDatabase(dbfile,**{})
	db.connect()
	dbproxy.initialize(db)

	impressions = []
	for review in Revlog.select():
		timestamp = datetime.datetime.fromtimestamp(float(review.id) / 1000.0)

		if review.ease == 1:
			type = 'failed'
		elif review.type == 0:
			type = 'learning'
		elif review.type == 1:
			type = 'review'
		elif review.type == 2:
			type = 'relearn'
		elif review.type == 3:
			type = 'filter'
		else:
			continue

		prototype = {
			'type': type,
			'time': review.time
		}
		impressions.append((timestamp,prototype))

	return impressions