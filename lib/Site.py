#!/usr/bin/python3
import os.path

class Site:
	def __init__( self):
		pass

	def add( self, page):
		os.makedirs( page.name)

	def remove( name):
		try:
			os.rmdir( name)
		except FileNotFoundError:
			raise
