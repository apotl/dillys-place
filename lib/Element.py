import random

class Element:
	def __init__( self, type):
		if type == 'text':
			self.type = 'text'
		else if type == 'image':
			self.type = 'image'
		else:
			raise
		self.content = ''
		self.location = ''
		random.seed()
		self.id = random.getrandbits(32)
	def renderElement():
		ele = {}
		ele['type'] = self.type
		ele['content'] = self.content
		ele['location'] = self.location
		ele['id'] = self.id
		return ele
		
