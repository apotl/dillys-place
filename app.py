from lib.Site import *
from lib.Page import *
from lib.Element import *
from lib.Forms import *
from lib.Render import *
from flask import Flask, request, render_template, redirect
from flask.ext.basicauth import BasicAuth
import json
import sys
import string
import html

if len( sys.argv) != 3:
	print( 'usage: ' + sys.argv[0] + ' secrets_file site_name')
	exit()

try:
	secrets = open( sys.argv[1], 'r')
	username = secrets.readline()
	password = secrets.readline()
	username = username.strip( '\n')
	password = password.strip( '\n')
	if len( username) == 0 or len( password) == 0:
		raise
	secrets.close()
except:
	print( 'Could not parse ' + sys.argv[1] + '. Exiting')
	exit()

if sys.argv[2] == 'lib' or sys.argv[2] == 'static' or sys.argv[2] == 'templates':
	print( 'Site name is invalid. Exiting')
	exit()

site = Site( sys.argv[2])
for char in site.name:
	if char not in string.ascii_letters + string.digits + '_':
		print( 'Site name is invalid. Exiting')
		exit()
site.name += '/'

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = username
app.config['BASIC_AUTH_PASSWORD'] = password

basic_auth = BasicAuth( app)

@app.route( '/')
def route_index():
	try:
		links = Navbar( site, 'index')
		eles = Body( site, 'index')
	except KeyError:
		return '404 Not Found.', 404
	return render_template( 'base.html', header = render_template( 'header.html', links = links.render(), body = render_template( 'body.html', eles = eles.render())))

@app.route( '/<path:page_name>/')
def route_everything( page_name):
	try:
		links = Navbar( site, page_name)
		eles = Body( site, page_name)
	except KeyError:
		return '404 Not Found.', 404
	return render_template( 'base.html', header = render_template( 'header.html', links = links.render(), body = render_template( 'body.html', eles = eles.render())))

@app.route( '/edit/', methods=['GET'])
@basic_auth.required
def edit_page():
	if request.method == 'POST':
		if request.form['to_edit']:
			return redirect( '/edit/' + request.form['to_edit'])
		if request.form['to_create']:
			site.add( Page( site.name + request.form['to_create']))
	page_create = PageCreateForm( request.form)
	page_create.to_create.data = ''
	page_edit = PageEditForm( request.form)
	page_edit.choose( site.render().keys())
	return render_template( 'edit.html', page_create = page_create, page_edit = page_edit)

@app.route( '/edit/goto/', methods=['POST'])
@basic_auth.required
def edit_page_goto():
	if request.form['to_edit'] == 'Choose a page to edit...':
		return redirect( '/edit/')
	return redirect( '/edit/' + request.form['to_edit'])

@app.route( '/edit/create/', methods=['POST'])
@basic_auth.required
def edit_page_create():
	if request.form['to_create'] and 'edit' not in request.form['to_create'] and 'static' not in request.form['to_create']:
		site.add( Page( site.name + request.form['to_create']))
	return redirect( '/edit/')

@app.route( '/edit/<path:page_name>/', methods=['POST', 'GET'])
@basic_auth.required
def edit_page_specific( page_name):
	if page_name not in site.render().keys():
		return redirect( '/edit/')
	ele_add = ElementAddForm( request.form)
	ele_add.to_add_title.data = ''
	ele_add.to_add_content.data = ''
	ele_remove = ElementRemoveForm( request.form)
	ele_remove.choose( site.render()[page_name].render())
	return render_template( 'edit_specific.html', ele_remove = ele_remove, ele_add = ele_add, page_name = page_name)

@app.route( '/edit/delete/<path:page_name>/', methods=['POST'])
@basic_auth.required
def edit_page_specific_delete( page_name):
	site.remove( page_name)
	return redirect( '/edit/')

@app.route( '/edit/add/<path:page_name>/', methods=['POST'])
@basic_auth.required
def edit_page_specific_add( page_name):
	ele_to_add = Element( 'text')
	if not request.form['to_add_content']:
		return redirect( '/edit/' + page_name)
	ele_to_add.title = request.form[ 'to_add_title']
	ele_to_add.content = request.form['to_add_content'].replace( '\n', ' ')
	ele_to_add.location = 'body'
	site.render()[page_name].add( ele_to_add)
	return redirect( '/edit/' + page_name)

@app.route( '/edit/remove/<path:page_name>/', methods=['POST'])
@basic_auth.required
def edit_page_specific_remove( page_name):
	if request.form['to_remove'] == '':
		return redirect( '/edit/' + page_name)
	site.render()[page_name].remove( request.form['to_remove'])
	return redirect( '/edit/' + page_name)

if __name__ == '__main__':
	app.run( host = '0.0.0.0', debug = True)
