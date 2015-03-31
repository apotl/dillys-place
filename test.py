#!/usr/bin/python3
from lib.Element import *
from lib.Page import *
from lib.Site import *
import random

def makeChoice():
	print( '\nSelect a lib to check: ' )
	print( '   (1) Element.py' )
	print( '   (2) Page.py' )
	print( '   (3) Site.py' )
	print( '   (e) Exit test.py' )
	choice = input()
	return choice

def checkElement_py():
	random.seed()
	print( 'Testing instantiation...')
	try:
		try:
			test_element = Element( 'text')
		except:
			print( 'Instantiation of Element type \'text\' failed...FAILURE')
			raise
		try:
			test_element = Element( 'image')
		except:
			print( 'Instantiation of Element type \'image\' failed...FAILURE.')
			raise
		try:
			test_element = Element( str( random.getrandbits( 32)))
			print( 'Instantiation of unspecified Element type succeeded...FAILURE.')
			raise
		except:
			pass
		print( 'Instantiation OK.' )
	except:
		pass

checking = True
while checking == True:
	choice = makeChoice()
	if choice == '1':
		checkElement_py()
	elif choice == '2':
#		checkPage_py()
		pass
	elif choice == '3':
#		checkSite_py()
		pass
	elif choice == 'e':
		checking = False
	else:
		print( 'ERROR: Given option invalid' )
