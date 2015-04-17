from lib.Site import *
from lib.Page import *
from lib.Element import *
from lib.Forms import *
from flask import Flask, request, render_template, redirect
from flask.ext.basicauth import BasicAuth
import json
import sys
import pprint

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

site = Site( sys.argv[2])

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = username
app.config['BASIC_AUTH_PASSWORD'] = password

basic_auth = BasicAuth( app)

@app.route( '/')
def route_index():
	if site.name + '/index' in site.render().keys():
		return 'well there\'s an index page...'
	else:
		return 'please add an index page!!'

@app.route( '/edit/', methods=['GET'])
@basic_auth.required
def edit_page():
	if request.method == 'POST':
		if request.form['to_edit']:
			return redirect( '/edit/' + request.form['to_edit'])
		if request.form['to_add']:
			site.add( Page( site.name + request.form['to_add']))
	page_add = PageAddForm( request.form)
	page_add.to_add.data = ''
	page_edit = PageEditForm( request.form)
	page_edit.choose( site.render().keys())
	return render_template( 'edit.html', page_add = page_add, page_edit = page_edit)

@app.route( '/edit/goto/', methods=['POST'])
@basic_auth.required
def edit_page_goto():
	return redirect( '/edit/' + request.form['to_edit'])

@app.route( '/edit/add/', methods=['POST'])
@basic_auth.required
def edit_page_add():
	if request.form['to_add']:
		site.add( Page( site.name + request.form['to_add']))
	return redirect( '/edit/')

@app.route( '/edit/<path:page_name>', methods=['POST', 'GET'])
@basic_auth.required
def edit_page_specific( page_name):
	return render_template( 'edit_specific.html', page_name = page_name)

@app.route( '/edit/<path:page_name>/delete/', methods=['POST', 'GET'])
@basic_auth.required
def edit_page_specific_delete( page_name):
	site.remove( page_name)
	return redirect( '/edit/')

if __name__ == '__main__':
	app.run( host = '0.0.0.0', debug = True)
