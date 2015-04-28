from lib.Site import *
from lib.Page import *
from lib.Element import *
from lib.Forms import *
from lib.Render import *
from flask import Flask, request, render_template, redirect, send_file
from flask.ext.basicauth import BasicAuth
from werkzeug import secure_filename
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

for char in sys.argv[2]:
	if char not in string.ascii_letters + string.digits + '_':
		print( 'Site name is invalid. Exiting')
		exit()
site = Site( sys.argv[2])
site.name += '/'

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = username
app.config['BASIC_AUTH_PASSWORD'] = password

basic_auth = BasicAuth( app)

ALLOWED_EXTENSIONS = set( [ 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file( filename): # thank you flask docs :)
	return '.' in filename and \
		filename.rsplit( '.', 1)[1] in ALLOWED_EXTENSIONS

@app.route( '/')
def route_index():
	try:
		links = Navbar( site, 'index')
		eles = Body( site, 'index')
	except KeyError:
		return '404 Not Found.', 404
	return render_template( 'base.html', header = render_template( 'header.html', links = links.render(), body = render_template( 'body_index.html', eles = eles.render())))

@app.route( '/<path:page_name>/')
def route_everything( page_name):
	try:
		links = Navbar( site, page_name)
		eles = Body( site, page_name)
	except KeyError:
		return '404 Not Found.', 404
	return render_template( 'base.html', header = render_template( 'header.html', links = links.render(), body = render_template( 'body_normal.html', eles = eles.render())))

@app.route( '/<path:page_name>/assets/<imagename>')
def route_assets( page_name, imagename):
	try:
		return send_file( site.name + page_name + '/assets/' + imagename)
	except:
		return '404 Not Found.', 404

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
	for char in request.form['to_create']:
		if char not in string.ascii_letters + string.digits + ' ':
			return redirect( '/edit/')
	if request.form['to_create'] and 'edit' not in request.form['to_create'] and 'static' not in request.form['to_create']:
		site.add( Page( site.name + request.form['to_create'].lower()))
	return redirect( '/edit/')

@app.route( '/edit/<path:page_name>/', methods=['POST', 'GET'])
@basic_auth.required
def edit_page_specific( page_name):
	if page_name not in site.render().keys():
		return redirect( '/edit/')
	ele_add = ElementAddForm( request.form)
	ele_add.to_add_title.data = ''
	ele_add.to_add_content.data = ''
	
	ele_add_image = ElementAddForm_Image( request.form)
	ele_add_image.to_add_title.data = ''

	ele_change = ElementChangeForm( request.form)
	ele_change.choose( site.render()[page_name].render())
	return render_template( 'edit_specific.html', ele_change = ele_change, ele_add = ele_add, ele_add_image = ele_add_image, page_name = page_name)

@app.route( '/edit/goto/<path:page_name>/', methods=['POST'])
@basic_auth.required
def edit_page_specific_goto( page_name):
	if request.form['to_change'] == '':
		return redirect( '/edit/' + page_name)
	return redirect( '/edit/' + page_name + '/id/' + request.form['to_change'])

@app.route( '/edit/delete/<path:page_name>/', methods=['POST'])
@basic_auth.required
def edit_page_specific_delete( page_name):
	site.remove( page_name)
	return redirect( '/edit/')

@app.route( '/edit/add/<path:page_name>/', methods=['POST'])
@basic_auth.required
def edit_page_specific_add( page_name):
	pprint.pprint( request.files)
	pprint.pprint( request.form)
	if 'to_add_content' not in request.form:
		ele_to_add = Element( 'image')
	else:
		ele_to_add = Element( 'text')
	ele_to_add.title = request.form['to_add_title']
	if ele_to_add.frmt == 'text':
		ele_to_add.content = request.form['to_add_content'].replace( '\n', ' ')
	else:
		image = request.files['to_add_image']
		print( 'works')
		imagename = secure_filename( image.filename)
		if not imagename:
			return redirect( '/edit/' + page_name)
		image.save( page_name + '/assets/' + imagename)
		ele_to_add.content = imagename
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

@app.route( '/edit/<path:page_name>/id/<ele_id>/', methods=['POST', 'GET'])
@basic_auth.required
def edit_page_specific_element( page_name, ele_id):
	if site.render()[page_name].retrieve( ele_id)['frmt'] == 'text':
		ele_change = ElementAddForm( request.form)
		ele_change.to_add_title.data = site.render()[page_name].render()[ele_id]['title']
		ele_change.to_add_content.data = site.render()[page_name].render()[ele_id]['content']
		return render_template( 'edit_specific_element.html', ele_change = ele_change, page_name = page_name, ele_id = ele_id)
	else:
		ele_change = ElementAddForm_Image( request.form)
		ele_change.to_add_title.data = site.render()[page_name].render()[ele_id]['title']
		return render_template( 'edit_specific_element_image.html', ele_change = ele_change, page_name = page_name, ele_id = ele_id)

@app.route( '/edit/<path:page_name>/id/change/<ele_id>/', methods=['POST'])
@basic_auth.required
def edit_page_specific_element_change( page_name, ele_id):
	tmp_ele = Element( site.render()[page_name].retrieve( ele_id)['frmt'])
	tmp_ele.load( site.render()[page_name].retrieve( ele_id))
	tmp_ele.title = request.form['to_add_title']
	if tmp_ele.frmt == 'text':
		tmp_ele.content = request.form['to_add_content']
	site.render()[page_name].remove( ele_id, skeleton = True)
	site.render()[page_name].add( tmp_ele)
	return redirect( '/edit/' + page_name)

@app.route( '/edit/<path:page_name>/id/remove/<ele_id>/', methods=['POST'])
@basic_auth.required
def edit_page_specific_element_remove( page_name, ele_id):
	site.render()[page_name].remove( ele_id)
	return redirect( '/edit/' + page_name)

if __name__ == '__main__':
	app.run( host = '0.0.0.0', debug = True)
