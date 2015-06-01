#!/usr/bin/python3
import random
import datetime

class ElementError( Exception):

	def __init__( self, reason):
		self.reason = 'ERROR in Element.py: ' + reason

class Element:
	def __init__( self, frmt):
		if frmt == 'text':
			self.frmt = 'text'
		elif frmt == 'image':
			self.frmt = 'image'
		elif frmt == 'event':
			self.frmt = 'event'
		elif frmt == 'blogpost':
			self.frmt = 'blogpost'
		else:
			raise ElementError( 'Invalid element type')
		self.title = ''
		self.content = ''
		self.location = ''
		self.distance = 0
		if self.frmt == 'image':
			self.caption = ''
		if self.frmt == 'event':
			self.when = ''
			self.where = ''
		if self.frmt == 'blogpost':
			self.postdate = datetime.datetime.now().strftime('%A %B %d, %Y')
			self.posttime = datetime.datetime.now().strftime('%I:%M %p')
		random.seed()
		self.id = str( random.getrandbits(32))
	def render( self):
		ele = {}
		ele['frmt'] = self.frmt
		ele['title'] = self.title
		ele['content'] = self.content
		ele['location'] = self.location
		ele['distance'] = self.distance
		ele['id'] = self.id
		if self.frmt == 'image':
			ele['caption'] = self.caption
		if self.frmt == 'event':
			ele['when'] = self.when
			ele['where'] = self.where
		if self.frmt == 'blogpost':
			ele['postdate'] = self.postdate
			ele['posttime'] = self.posttime
		return ele
	def load( self, ele_dict):
		try:
			self.frmt = ele_dict['frmt']
			self.title = ele_dict['title']
			self.content = ele_dict['content']
			self.location = ele_dict['location']
			self.distance = ele_dict['distance']
			self.id = ele_dict['id']
			if self.frmt == 'image':
				self.caption = ele_dict['caption']
			if self.frmt == 'event':
				self.when = ele_dict['when']
				self.where = ele_dict['where']
			if self.frmt == 'blogpost':
				self.postdate = ele_dict['postdate']
				self.posttime = ele_dict['posttime']
		except:
			raise ElementError( 'given element dict is invalid')
