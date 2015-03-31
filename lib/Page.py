#!/usr/bin/python3
import os.path
import json

class Page:
	def __init__( self, name):
		if not os.path.isdir( name):
			raise
		self.name = name

	def add( self, ele):
		try:
			ele['frmt']
			ele['content']
			ele['location']
			ele['id']
		except KeyError:
			raise
		ele_file = open( self.name + '/' + ele['id'], 'r+')
		ele_file.write( json.dumps( ele))
		ele_file.close()

	def remove( self, ele_id):
		try:
			os.remove( self.name + '/' + ele_id)
		except FileNotFoundError:
			raise

	def retrieve( self, ele_id):
		try:
			ele_file = open( self.name + '/' + ele_id)
		except FileNotFoundError:
			raise
		ele_content = ele_file.read()
		ele_file.close()
		return json.loads( ele_content)
	
	def render( self): #will pass all elements in a dictionary
		pass
