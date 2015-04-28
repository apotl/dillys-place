from wtforms import Form, TextField, SelectField, TextAreaField, FileField
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
		if not tmp_ele.title:
			to_ret += [ ( tmp_ele.distance, tmp_ele.id, '"' + tmp_ele.content[:25] + checkElementContentLength( tmp_ele.content) + '"')]
		else:
			to_ret += [ ( tmp_ele.distance, tmp_ele.id, 'TITLE: ' + tmp_ele.title)]
	to_ret = sorted( to_ret)
	to_rly_ret = []
	for ele in to_ret:
		to_rly_ret += [ ( ele[1], ele[2])]
	return to_rly_ret


class PageEditForm( Form):
	to_edit = SelectField( 'Page Name')
	
	def choose( self, pages):
		self.to_edit.choices = listToPair( pages)
		self.to_edit.choices.insert( 0, ( 'Choose a page to edit...', 'Choose a page to edit...'))

class ElementAddForm( Form):
	to_add_title = TextField( 'Element Title')
	to_add_content = TextAreaField( 'Element Content')

class ElementAddForm_Image( Form):
	to_add_title = TextField( 'Image Title')
	to_add_image = FileField( 'Image File')
	to_add_caption = TextAreaField( 'Image Caption')

class ElementChangeForm( Form):
	to_change = SelectField( 'Element Name')
	
	def choose( self, elements):
		self.to_change.choices = renderElementList( elements)
		self.to_change.choices.insert( 0, ( '', '***Choose an element to change***'))
