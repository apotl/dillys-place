#!/usr/bin/python3
import os.path
import json
import pprint

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
		self._maxdist = self.__find_maxdist()

	def __find_maxdist( self):
		maxlist = []
		dict_render = self.render()
		for ele in dict_render.keys():
			maxlist += [ dict_render[ele]['distance'] ]
		if maxlist == []:
			return 0
		return max( maxlist)

	def add( self, ele, old = False):
		try:
			ele.frmt
			ele.title
			ele.content
			ele.location
			ele.distance
			ele.id
		except AttributeError:
			raise PageError( 'Element given is invalid')
		if not old:
			ele.distance = self._maxdist + 10
			self._maxdist = ele.distance
		ele_file = open( self.name + '/' + ele.id, 'w+')
		ele_file.write( json.dumps( ele.render()))
		ele_file.close()

	def remove( self, ele_id):
		try:
			os.remove( self.name + '/' + ele_id)
		except FileNotFoundError:
			raise PageError( 'Element id given does not exist')
		self._maxdist = self.__find_maxdist()

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
