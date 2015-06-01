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
def allowed_file( filename):
	return '.' in filename and \
		filename.rsplit( '.', 1)[1] in ALLOWED_EXTENSIONS

@app.route( '/')
def route_index():
	try:
		links = Navbar( site, 'index')
		eles = Body( site, 'index')
	except KeyError:
		return '404 Not Found.', 404
	return render_template( 'base.html', title = 'Home', header = render_template( 'header.html', links = links.render(), body = render_template( 'body_index.html', editloc = site.name + 'index', eles = eles.render())))

@app.route( '/<path:page_name>/')
def route_everything( page_name):
	try:
		links = Navbar( site, page_name)
		eles = Body( site, page_name)
	except KeyError:
		return '404 Not Found.', 404
	return render_template( 'base.html', title = page_name.capitalize(), header = render_template( 'header.html', links = links.render(), body = render_template( 'body.html', editloc = site.name + page_name, eles = eles.render())))

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
	return render_template( 'bedit.html', edits = render_template( 'edit.html', page_create = page_create, page_edit = page_edit))

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
	ele_add_image.to_add_caption.data = ''

	ele_add_event = ElementAddForm_Event( request.form)
	ele_add_event.to_add_title.data = ''
	ele_add_event.to_add_content.data = ''
	ele_add_event.to_add_when.data = ''
	ele_add_event.to_add_where.data = ''

	ele_add_blogpost = ElementAddForm_Blogpost( request.form)
	ele_add_blogpost.to_add_title.data = ''
	ele_add_blogpost.to_add_content.data = ''
	ele_add_blogpost.to_add_posttime.data = 'p' #placeholder
	ele_add_blogpost.to_add_postdate.data = 'p' #placeholder
	
	ele_change = ElementChangeForm( request.form)
	ele_change.choose( site.render()[page_name].render())
	if page_name == site.name + 'index':
		return render_template( 'bedit.html', edits = render_template( 'edit_specific_indexpage.html', ele_change = ele_change, ele_add = ele_add, ele_add_image = ele_add_image, page_name = page_name))
	if page_name == site.name + 'events':
		return render_template( 'bedit.html', edits = render_template( 'edit_specific_eventspage.html', ele_change = ele_change, ele_add_event = ele_add_event, page_name = page_name))
	if page_name == site.name + 'photos':
		return render_template( 'bedit.html', edits = render_template( 'edit_specific_photospage.html', ele_change = ele_change, ele_add_image = ele_add_image, page_name = page_name))
	if page_name == site.name + 'blog':
		return render_template( 'bedit.html', edits = render_template( 'edit_specific_blogpage.html', ele_change = ele_change, ele_add_blogpost = ele_add_blogpost, page_name = page_name))
	return render_template( 'bedit.html', edits = render_template( 'edit_specific.html', ele_change = ele_change, ele_add = ele_add, ele_add_image = ele_add_image, page_name = page_name))

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
	if 'to_add_content' not in request.form:
		ele_to_add = Element( 'image')
	elif 'to_add_when' and 'to_add_where' in request.form:
		ele_to_add = Element( 'event')
	elif 'to_add_postdate' and 'to_add_posttime' in request.form:
		ele_to_add = Element( 'blogpost')
	else:
		ele_to_add = Element( 'text')
	ele_to_add.title = request.form['to_add_title']
	if ele_to_add.frmt == 'text':
		ele_to_add.content = request.form['to_add_content'].replace( '\n', '<br>')
	elif ele_to_add.frmt == 'image':
		image = request.files['to_add_image']
		imagename = secure_filename( image.filename)
		if not imagename:
			return redirect( '/edit/' + page_name)
		image.save( page_name + '/assets/' + imagename)
		ele_to_add.content = imagename
		ele_to_add.caption = request.form['to_add_caption'].replace( '\n', '<br>')
	elif ele_to_add.frmt == 'event':
		ele_to_add.content = request.form['to_add_content'].replace( '\n', '<br>')
		ele_to_add.when = request.form['to_add_when'].replace( '\n', '<br>')
		ele_to_add.where = request.form['to_add_where']
	elif ele_to_add.frmt == 'blogpost':
		ele_to_add.content = request.form['to_add_content'].replace( '\n', '<br>')

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
		ele_change.to_add_content.data = site.render()[page_name].render()[ele_id]['content'].replace( '<br>', '\n')
		return render_template( 'bedit.html', edits = render_template( 'edit_specific_element.html', ele_change = ele_change, page_name = page_name, ele_id = ele_id))
	elif site.render()[page_name].retrieve( ele_id)['frmt'] == 'image':
		ele_change = ElementAddForm_Image( request.form)
		ele_change.to_add_title.data = site.render()[page_name].render()[ele_id]['title']
		ele_change.to_add_image.data = site.render()[page_name].render()[ele_id]['content']
		ele_change.to_add_caption.data = site.render()[page_name].render()[ele_id]['caption'].replace( '<br>', '\n')
		return render_template( 'bedit.html', edits = render_template( 'edit_specific_element_image.html', ele_change = ele_change, page_name = page_name, ele_id = ele_id, imagename = '/' + page_name[len( site.name):] + '/assets/' + site.render()[page_name].render()[ele_id]['content']))
	elif site.render()[page_name].retrieve( ele_id)['frmt'] == 'event':
		ele_change = ElementAddForm_Event( request.form)
		ele_change.to_add_title.data = site.render()[page_name].render()[ele_id]['title']
		ele_change.to_add_content.data = site.render()[page_name].render()[ele_id]['content'].replace( '<br>', '\n')
		ele_change.to_add_when.data = site.render()[page_name].render()[ele_id]['when'].replace( '<br>', '\n')
		ele_change.to_add_where.data = site.render()[page_name].render()[ele_id]['where']
		return render_template( 'bedit.html', edits = render_template( 'edit_specific_element_event.html', ele_change = ele_change, page_name = page_name, ele_id = ele_id))
	elif site.render()[page_name].retrieve( ele_id)['frmt'] == 'blogpost':
		ele_change = ElementAddForm_Blogpost( request.form)
		ele_change.to_add_title.data = site.render()[page_name].render()[ele_id]['title']
		ele_change.to_add_content.data = site.render()[page_name].render()[ele_id]['content'].replace( '<br>', '\n')
		return render_template( 'bedit.html', edits = render_template( 'edit_specific_element_blogpost.html', ele_change = ele_change, page_name = page_name, ele_id = ele_id))

@app.route( '/edit/<path:page_name>/id/change/<ele_id>/', methods=['POST'])
@basic_auth.required
def edit_page_specific_element_change( page_name, ele_id):
	tmp_ele = Element( site.render()[page_name].retrieve( ele_id)['frmt'])
	tmp_ele.load( site.render()[page_name].retrieve( ele_id))
	tmp_ele.title = request.form['to_add_title']
	if tmp_ele.frmt == 'text':
		tmp_ele.content = request.form['to_add_content']
	elif tmp_ele.frmt == 'image':
		image = request.files['to_add_image']
		if image:
			imagename = secure_filename( image.filename)
			image.save( page_name + '/assets/' + imagename)
			tmp_ele.content = imagename
		tmp_ele.caption = request.form['to_add_caption']
	elif tmp_ele.frmt == 'event':
		tmp_ele.content = request.form['to_add_content']
		tmp_ele.when = request.form['to_add_when']
		tmp_ele.where = request.form['to_add_where']
	elif tmp_ele.frmt == 'blogpost':
		tmp_ele.content = request.form['to_add_content']
	site.render()[page_name].remove( ele_id, skeleton = True)
	site.render()[page_name].add( tmp_ele, old = True)
	return redirect( '/edit/' + page_name)

@app.route( '/edit/<path:page_name>/id/remove/<ele_id>/', methods=['POST'])
@basic_auth.required
def edit_page_specific_element_remove( page_name, ele_id):
	site.render()[page_name].remove( ele_id)
	return redirect( '/edit/' + page_name)

if __name__ == '__main__':
	app.run( host = '0.0.0.0', debug = True)
