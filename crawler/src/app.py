#!/usr/bin/python
from flask import Flask
from flask import jsonify

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
app.config['CORS_HEADERS'] = 'Content-Type'

#
# index
#
@app.route('/<crawlerName>/<timeLength>/<token>', methods=["POST"])
def submitError(crawlerName, timeLength, token):
	# validate
	if token != 'hello':
		return 'nice try.'
	# run script
	output = getattr(crawlers, crawlerName).main(stock)
	# return output
	return '200. I got the data and put it in the database for ya ;)'




if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8083, threaded=True, debug=True)