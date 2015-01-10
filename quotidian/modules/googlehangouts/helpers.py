import datetime, time

class HangoutsData:
	"""Takes in the raw objectified json data and makes it a little more
	manageable."""
	def __init__(self,data):
		self.data = data
		self.knownUsers = {}

	def conversations(self):
		return map(lambda convo: Conversation(convo['conversation_state'],self), self.data['conversation_state'])




class Conversation:

	def __init__(self,data,main):
		self.data = data
		self.main = main

	def name(self):
		return self.data['conversation']['name']

	def id(self):
		return self.data['conversation']['id']['id']

	def participants(self):
		for participant in self.data['conversation']['participant_data']:
			if not 'fallback_name' in participant:
				if participant['id']['gaia_id'] in self.main.knownUsers:
					participant['fallback_name'] = self.main.knownUsers[participant['id']['gaia_id']]
				else:
					participant['fallback_name'] = None

		participants = map(lambda participant: User(participant['id']['gaia_id'],
										            participant['fallback_name'],
										            self.main), 
				   self.data['conversation']['participant_data'])
		
		for participant in participants:
			if not participant.id in self.main.knownUsers:
				if participant.name != None:
					self.main.knownUsers[participant.id] = participant.getName()

		return participants

	def participantNames(self):
		return [participant.getName() for participant in self.participants()]

	def participantById(self,id):
		for participant in self.participants():
			if participant.id == id:
				return participant
		return None

	def currentParticipants(self):
		return map(lambda participant: self.participantById(participant['id']),
				   self.data['conversation']['current_participant'])

	def messages(self):
		return map(lambda e: Message(e,self.participantById(e['sender_id']['gaia_id'])),
				   self.data['event'])

class Message:

	def __init__(self,data,sender):
		self.data = data
		self.sender = sender

	def text(self):
		if self.type() == 'chat_message':
			message = ""
			if 'segment' in self.data['chat_message']['message_content']:
				return ' '.join([part['text'] for part in self.data['chat_message']['message_content']['segment'] if 'text' in part])
		else:
			return ""

	def segmentCount(self):
		if self.type() == 'chat_message' and 'segment' in self.data['chat_message']['message_content']:
			return len(self.data['chat_message']['message_content']['segment'])
		else:
			return 0

	def type(self):
		props = self.data.keys()
		if 'chat_message' in props:
			return 'chat_message'
		elif 'membership_change' in props:
			return 'membership_change'
		elif 'hangout_event' in props or 'conversation_rename' in props:
			return 'hangout_event'

	def date(self):
		seconds = float(self.data['timestamp']) / 1000000.0
		# Holy shit that's a precise value
		return datetime.datetime.fromtimestamp(seconds)

class User:

	def __init__(self,id,name,main):
		self.id = id
		self.name = name
		self.main = main

	def __str__(self):
		return '%s: %s' % (self.id,self.getName())

	def getName(self):
		if self.name != None:
			return self.name
		else:
			if self.id in self.main.knownUsers:
				self.name = self.main.knownUsers[self.id]
				return self.getName()
			else:
				return None