from lib.Site import *
from lib.Page import *
from lib.Element import *
from lib.Forms import *
from flask import Flask, request, render_template
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

@app.route( '/edit', methods=['POST', 'GET'])
@basic_auth.required
def edit_page():
	if request.method == 'POST':
		pass
		site.add( Page( site.name + request.form['page_name']))
	form = PageAddForm( request.form)
	form.page_name.data = ''
	pages = list( site.render().keys())
	pprint.pprint( pages)
	return render_template( 'edit.html', form = form, pages = pages)

if __name__ == '__main__':
	app.run( host = '0.0.0.0', debug = True)
