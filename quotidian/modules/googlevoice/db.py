from peewee import *

dbConnection = Proxy()

class Query(Model):
	id = IntegerField(primary_key=True)
	query = TextField()
	class Meta:
		database = dbConnection