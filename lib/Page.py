#!/usr/bin/python3
import os.path
import json

class PageError( Exception):

	def __init__( self, reason):
		self.reason = 'ERROR in Page.py: ' + reason

class Page:
	def __init__( self, name):
		try:
			if not os.path.isdir( name):
				os.mkdir( name)
		except:
			raise PageError( 'Could not create a directory with that name')
		self.name = name

	def add( self, ele):
		try:
			ele.frmt
			ele.content
			ele.location
			ele.id
		except AttributeError:
			raise PageError( 'Element given is invalid')
		ele_file = open( self.name + '/' + ele.id, 'w+')
		ele_file.write( json.dumps( ele.render()))
		ele_file.close()

	def remove( self, ele_id):
		try:
			os.remove( self.name + '/' + ele_id)
		except FileNotFoundError:
			raise PageError( 'Element id given does not exist')

	def retrieve( self, ele_id):
		try:
			ele_file = open( self.name + '/' + ele_id)
		except FileNotFoundError:
			raise PageError( 'Element id given does not exist')
		ele_content = ele_file.read()
		ele_file.close()
		return json.loads( ele_content)
	
	def render( self): #will pass all elements in a dictionary
		dict_render = {}
		for element in os.listdir( self.name):
			dict_render[element] = self.retrieve( element)
		return dict_render
	
	def __del__( self):
		to_rm = self.render()
		for element in to_rm:
			self.remove( to_rm.get( element)['id'])
		os.rmdir( self.name)
