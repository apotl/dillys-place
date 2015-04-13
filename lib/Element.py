#!/usr/bin/python3
import random

class ElementError( Exception):

	def __init__( self, reason):
		self.reason = 'ERROR in Element.py: ' + reason

class Element:
	def __init__( self, frmt):
		if frmt == 'text':
			self.frmt = 'text'
		elif frmt == 'image':
			self.frmt = 'image'
		else:
			raise ElementError( 'Invalid element type')
		self.content = ''
		self.location = ''
		random.seed()
		self.id = str( random.getrandbits(32))
	def render( self):
		ele = {}
		ele['frmt'] = self.frmt
		ele['content'] = self.content
		ele['location'] = self.location
		ele['id'] = self.id
		return ele
		
