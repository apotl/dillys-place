#!/usr/bin/python3
import os.path
from lib.Page import *

class SiteError( Exception):

	def __init__( self, reason):
		self.reason = 'ERROR in Site.py: ' + reason

class Site:
	def __init__( self, name):
		try:
			if not os.path.isdir( name):
				os.mkdir( name)
			else:
				raise SiteError( 'New site cannot be an existing directory')
		except:
			raise SiteError( 'Could not create a directory with that name')
		self.name = name
		self.tree = {}

	def add( self, page):
		self.tree[page.name] = page

	def render( self):
		return self.tree

	def remove( self, name):
		try:
			del self.tree[name]
		except:
			raise SiteError( 'Could not remove page successfully')
