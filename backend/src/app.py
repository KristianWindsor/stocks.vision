#!/usr/bin/python
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS, cross_origin
import os
import pymysql
import json
import datetime
from datetime import datetime, date, timedelta
import dateutil.relativedelta
import requests
from random import randrange

# write each module name in __init__.py so they can import successfully
from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "indicators/*.py"))
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
text_file = open("indicators/__init__.py", "w")
text_file.write('__all__ = ' + str(__all__) + '\nfrom . import *')
text_file.close()
import indicators
import simulation


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
	data = request.get_json()
	indicator = data['indicator']
	stock = data['stock']
	date = data['date']
	# run indicator py script with given stock
	results = {}
	if isinstance(indicator, (list,)):
		print('this is a list')
	elif indicator == '*':
		print('star. return all indicator values')
		indicatorNameList = []
		for root, dirs, files in os.walk(r'indicators/'):
			for file in files:
				if file.endswith('.py') and '__init__' not in file:
					indicatorNameList.append(file.replace('.py', ''))
		for indicatorName in indicatorNameList:
			results[indicatorName] = getattr(indicators, indicatorName).main(stock, date)
		print(results)
	else:
		print('this is a single indicator')
		results[indicator] = getattr(indicators, indicator).main(stock, date)
	return jsonify(results)


#
# simulation
#
@app.route('/simulation', methods=["POST"])
@cross_origin()
def runSimulation():
	data = request.get_json()
	stock = data['stock']
	cash = 10000.00
	indicators = data['indicators']
	endDate = datetime.now().date()
	print('endDate')
	print(endDate)
	startDate = endDate - dateutil.relativedelta.relativedelta(weeks=data['length']) # should be date, not datetime
	# get results
	results = simulation.RunSimulation.main(stock, indicators, startDate, endDate, cash)
	# return results
	return results


#
# simulation analyze
#
@app.route('/simulationAnalyze', methods=["POST"])
@cross_origin()
def simulationAnalyze():
	# > here are the completed simulations
	# > please give me one that's better
	data = request.get_json()
	stock = data['stock']
	completedSimulations = data['completedSimulations']
	indicators = data['indicators']
	cash = 10000.00
	endDate = datetime.now()
	startDate = endDate - dateutil.relativedelta.relativedelta(weeks=data['length'])
	# run simulation 
	# if not better, run again
	# return data
	currentHighestGain = 0
	for cs in completedSimulations:
		if completedSimulations[cs] > currentHighestGain:
			currentHighestGain = completedSimulations[cs]
	returnData = {
		'gain': 0
	}
	cnt = 0
	while returnData['gain'] <= currentHighestGain and cnt < 100:
		# decide indicator settings
		indicatorConfigID = None
		while indicatorConfigID in completedSimulations or indicatorConfigID is None:
			indicatorConfigID = ''
			newIndicators = {}
			for indicatorName in indicators:
				newVal = randrange(-10,10)
				if newVal != 0:
					newIndicators[indicatorName] = newVal
					indicatorConfigID += indicatorName
					if len(newIndicators) != 1:
						indicatorConfigID += str(newIndicators[indicatorName])
		returnData = simulation.RunSimulation.main(stock, newIndicators, startDate, endDate, cash)
		cnt += 1
	return returnData

#
# stock ticker list
#
@app.route('/tickerlist', methods=["GET"])
@cross_origin()
def tickerlist():
	db = pymysql.connect(
		host=os.environ['MYSQL_HOSTNAME'],
		user='backend',
		passwd='pass',
		db='stocksvision',
		autocommit=True
	)
	cursor = db.cursor(pymysql.cursors.DictCursor)
	listOfAllStocks = []
	cursor.execute("SELECT ticker FROM stocks")
	for row in cursor.fetchall():
		listOfAllStocks.append(row['ticker'])
	return json.dumps(listOfAllStocks)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)