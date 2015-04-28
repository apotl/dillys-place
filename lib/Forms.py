from wtforms import Form, TextField, SelectField, TextAreaField
from lib.Element import *
import pprint

class PageCreateForm( Form):
	to_create = TextField( 'Page Name')

def listToPair( list):
	to_ret = []
	for page in list:
		to_ret += [ ( page, page)]
	return to_ret

def checkElementContentLength( content):
	if len( content) > 25:
		return '...'
	return ''

def renderElementList( list):
	to_ret = []
	for ele in list.keys():
		tmp_ele = Element( 'text')
		tmp_ele.load( list[ele])
		to_ret += [ ( tmp_ele.id, '"' + tmp_ele.content[:25] + checkElementContentLength( tmp_ele.content) + '"')]
	return to_ret


class PageEditForm( Form):
	to_edit = SelectField( 'Page Name')
	
	def choose( self, pages):
		self.to_edit.choices = listToPair( pages)
		self.to_edit.choices.insert( 0, ( 'Choose a page to edit...', 'Choose a page to edit...'))

class ElementAddForm( Form):
	to_add = TextAreaField( 'Element Content')

class ElementRemoveForm( Form):
	to_remove = SelectField( 'Element Name')
	
	def choose( self, elements):
		self.to_remove.choices = renderElementList( elements)
	#	self.to_remove.choices = []
		self.to_remove.choices.insert( 0, ( '', '***Choose an element to remove***'))
