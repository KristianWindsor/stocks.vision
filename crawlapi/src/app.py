#!/usr/bin/python
from flask import Flask
from flask import jsonify
from flask import request

# write each module name in __init__.py so they can import successfully
from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "crawlers/*.py"))
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
text_file = open("crawlers/__init__.py", "w")
text_file.write('__all__ = ' + str(__all__) + '\nfrom . import *')
text_file.close()
import crawlers


app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-type: application/json'


#
# Run Script
#
@app.route('/', methods=["GET"])
def index():
	return '200. we are ready to go.'
#
# Run Script
#
@app.route('/runScript', methods=["POST"])
def runScript():
	data = request.json
	crawlerName = data['crawlerName']
	startDate = data['startDate']
	token = data['token']
	print(crawlerName)
	print(startDate)
	print(token)
	# validate
	if token != 'hello':
		return 'nice try.'
	# run script
	output = getattr(crawlers, crawlerName).main()
	#return token
	return '200. I got the data and put it in the database for ya ;)'




if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8083, threaded=True, debug=True)