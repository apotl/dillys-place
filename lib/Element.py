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
		self.title = ''
		self.content = ''
		self.location = ''
		random.seed()
		self.id = str( random.getrandbits(32))
	def render( self):
		ele = {}
		ele['frmt'] = self.frmt
		ele['title'] = self.title
		ele['content'] = self.content
		ele['location'] = self.location
		ele['id'] = self.id
		return ele
	def load( self, ele_dict):
		try:
			self.frmt = ele_dict['frmt']
			self.title = ele_dict['title']
			self.content = ele_dict['content']
			self.location = ele_dict['location']
			self.id = ele_dict['id']
		except:
			raise ElementError( 'given element dict is invalid')
