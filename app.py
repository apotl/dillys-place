from lib.Site import *
from lib.Page import *
from lib.Element import *
from flask import Flask, request
import sys
import pprint

if len( sys.argv) != 2:
	print( 'usage: ' + sys.argv[0] + ' ' + 'site_name')
	exit()

site = Site( sys.argv[1])

app = Flask(__name__)

@app.route( '/')
def route_index():
	if site.name + '/index' in site.render().keys():
		return 'well there\'s an index page...'
	else:
		return 'please add an index page!!'

if __name__ == '__main__':
	app.run( host = '0.0.0.0')
