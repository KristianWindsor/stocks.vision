#!/usr/bin/python
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS, cross_origin
import os

# write each module name in __init__.py so they can import successfully
from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "indicators/*.py"))
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
text_file = open("indicators/__init__.py", "w")
text_file.write('__all__ = ' + str(__all__) + '\nfrom . import *')
text_file.close()
import indicators


app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#
# index
#
@app.route('/')
def index():
    return "Hey! You're not supposed to be here!"


#
# indicator
#
@app.route('/indicator', methods=["POST"])
@cross_origin()
def indicator():
	indicator = request.form.get('indicator')
	stock = request.form.get('stock')
	# run indicator py script with given stock
	# return results
	if isinstance(indicator, (list,)):
		print('this is a list')
		results = 'list'
	elif indicator == '*':
		print('star. return all indicator values')
		indicatorNameList = []
		results = {}
		for root, dirs, files in os.walk(r'indicators/'):
			for file in files:
				if file.endswith('.py') and '__init__' not in file:
					indicatorNameList.append(file.replace('.py', ''))
		for indicatorName in indicatorNameList:
			results[indicatorName] = getattr(indicators, indicatorName).main(stock)
		print(results)
	else:
		print('this is a single indicator')
		results = getattr(indicators, indicator).main(stock)
	return jsonify(results)


#
# simulation
#
@app.route('/simulation', methods=["POST"])
@cross_origin()
def simulation():
	stock = request.form.get('stock')
	holdDuration = request.form.get('holdDuration')
	indicatorData = request.form.get('indicators')
	completedSimulations = request.form.get('completedSimulations')
	# calculate which simulations to run based off of completedSimulations
	# run simulation
	# return results
	return '200 OK'


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)