info = {
	'name': 'Google Queries Importer',
	'version': 1.0,
	'description': """This can't really be used by the average user as of right
now, because it relies on a special database of queries that is scraped by
a different little script of mine. Normally, Google does not allow you to
download your queries, and the manner of getting them is rather roundabout and
not all that practical to distribute. Therefore, it's best just to leave this 
be until I can find a good way of implementing this for everyone."""
}

from db import *
from peewee import *
import os, datetime

def check(path):
	dbfile = path + '/queries.db'

	if not os.path.exists(dbfile):
		return False

	db = SqliteDatabase(dbfile)
	db.connect()
	dbConnection.initialize(db)

	try:
		Query.get()
	except:
		return False

	return True

def parse(path):
	dbfile = path + '/queries.db'
	db = SqliteDatabase(dbfile)
	db.connect()
	dbConnection.initialize(db)

	queries = []
	for query in Query.select():
		timestamp = datetime.datetime.fromtimestamp(query.id)
		prototype = {'query': query.query}
		queries.append((timestamp,prototype))

	return queries