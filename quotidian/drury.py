#!/usr/bin/env python

from peewee import *
import json, datetime

dbproxy = Proxy()

""" Sort of frustrating that this all has to sit in the global scope in this
file. Peewee doesn't really provide a good way of instantiating all of this,
so it's just sort of left up as an exercise to the reader and I'm not sure
what to do about it. In theory it will never be a problem, but I don't like it
one bit."""

class DBConnectModel(Model):
	class Meta:
		database = dbproxy

class DataPoint(DBConnectModel):
	timestamp = DateTimeField()
	module = CharField()
	data = TextField()

class BakeInfo(DBConnectModel):
	moduleName = CharField(primary_key=True)
	lastBaked = DateTimeField()


"""Why is this class called Drury? Well, it bakes our data, of course."""
class Drury:
	db = None

	def __init__(self,pathToDB):
		sqlitedb = SqliteDatabase(pathToDB)
		sqlitedb.connect()
		dbproxy.initialize(sqlitedb)

		self.db = sqlitedb
		self.db.create_tables([DataPoint,BakeInfo],safe=True)

	def bakeData(self,moduleName,data):
		# Clean out all old data
		DataPoint.delete().where(DataPoint.module == moduleName).execute()

		# Set up the data to be inserted
		encode = []
		for item in data:
			try:
				encoded = json.dumps(item[1]).encode('utf-8')
			except:
				print "Failed to encode"
				print [item[1]]
				exit()
			obj = {
				'timestamp': item[0], 
				'module': moduleName,
				'data': encoded
			}
			encode.append(obj)

		# Insert 'em
		size = 200
		times = len(encode) / size
		remaining = len(encode) % size != 0
		
		# Chunk
		for i in range(times):
			with self.db.transaction():
				DataPoint.insert_many(encode[i*size:(i+1)*size]).execute()

		# remaining
		with self.db.transaction():
			DataPoint.insert_many(encode[times*size:(times*size)+remaining]).execute()

		now = datetime.datetime.now()
		try:
			info = BakeInfo.get(BakeInfo.moduleName == moduleName)
			info.lastBaked = now
			info.save()
		except DoesNotExist:
			info = BakeInfo.create(moduleName = moduleName, lastBaked = now)

	def retrieveData(self,start,finish,moduleName):
		q = DataPoint.select().where(DataPoint.module == moduleName,
									      DataPoint.timestamp <= finish,
									      DataPoint.timestamp >= start)
		restoredData = []
		for point in q:
			restoredData.append((point.timestamp,json.loads(point.data,'utf-8')))

		return restoredData

	def lastBaked(self,moduleName):
		try:
			info = BakeInfo.get(BakeInfo.moduleName == moduleName)
			return info.lastBaked
		except DoesNotExist:
			return None

	def hasData(self,moduleName):
		try:
			info = BakeInfo.get(BakeInfo.moduleName == moduleName)
			return True
		except DoesNotExist:
			return False