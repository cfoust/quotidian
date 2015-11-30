info = {
	'name': 'Google Queries Importer',
	'version': 1.2,
	'description': """Google now provides you with all of the queries you have
	ever made on their website at https://history.google.com/history/. Click the
	three vertical dots in the upper right corner of the page (after you've 
	logged in) and click \"Download Searches\". You will get a zip archive in
	your email inbox. Copy the Searches folder (the nested one with all the files,
	not the one with index.html in it) into this module's folder."""
}

import os, datetime, json

def check(path):
	maindir = path + '/Searches/'

	if not os.path.exists(maindir):
		return False

	for f in os.listdir(maindir):
		if not f.endswith('.json'):
			return False

	return True



def parse(path):
	maindir = path + '/Searches/'

	queries = []
	for f in os.listdir(maindir):
		with open(maindir + f,'r') as json_file:
			obj = json.loads(json_file.read())

			for item in obj['event']:
				timestamp = float(item['query']['id'][0]['timestamp_usec']) / 1000000.0
				timestamp = datetime.datetime.fromtimestamp(timestamp)

				queries.append((timestamp,{'query': item['query']['query_text']}))

	return queries