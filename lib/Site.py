#!/usr/bin/python3
import os.path
import shutil
from lib.Element import *
from lib.Page import *

class SiteError( Exception):

	def __init__( self, reason):
		self.reason = 'ERROR in Site.py: ' + reason

class Site:
	def __init__( self, name):
		try:
			if not os.path.isdir( name):
				os.mkdir( name)
		except:
			raise SiteError( 'Could not create a directory with that name')
		self.name = name
		self.tree = {}
		page_list = os.listdir( self.name)
		page_dict = {}
		for page in page_list:
			page_dict[self.name + '/' + page] = os.listdir( self.name + '/' + page)
		for page_name in page_dict:
			page = Page( page_name)
			for element in page_dict[page_name]:
				try:
					ele_file = open( page_name + '/' + element)
					ele_content = ele_file.read()
					ele_file.close()
					ele_to_load = Element( 'text')
					ele_to_load.load( json.loads( ele_content))
					if element == ele_to_load.render()['id']:
						page.add( ele_to_load, old = True)
					else:
						print( 'Element to load to page is non-natively generated: ' + element)
				except IsADirectoryError:
					pass
				except:
					print( 'Element to load to page is non-natively generated: ' + element)
			self.tree[page_name] = page
		if name + '/index' not in page_dict:
			self.tree[name + '/index'] = Page( name + '/index')
		if name + '/events' not in page_dict:
			self.tree[name + '/events'] = Page( name + '/events')
		if name + '/photos' not in page_dict:
			self.tree[name + '/photos'] = Page( name + '/photos')
		if name + '/blog' not in page_dict:
			self.tree[name + '/blog'] = Page( name + '/blog')

	def add( self, page):
		self.tree[page.name] = page

	def render( self):
		return self.tree

	def remove( self, name):
		try:
			del self.tree[name]
			shutil.rmtree( name)
		except:
			raise SiteError( 'Could not remove page successfully')

