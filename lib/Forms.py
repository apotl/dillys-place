from wtforms import Form, TextField

class PageAddForm( Form):
	page_name = TextField( 'Page Name')
