from wtforms import Form, TextField, SelectField
import pprint

class PageAddForm( Form):
	to_add = TextField( 'Page Name')

def listToPair( list):
	to_ret = []
	for ele in list:
		to_ret += [ ( ele, ele)]
	return to_ret

class PageEditForm( Form):
	to_edit = SelectField( 'Page Name')
	
	def choose( self, pages):
		self.to_edit.choices = listToPair( pages)
