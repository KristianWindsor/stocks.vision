#!/usr/bin/python
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import os, pymysql, json, datetime, requests
from datetime import datetime, timedelta
import dateutil.relativedelta
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
import backtest


app = Flask(__name__)
CORS(app)


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
# backtest
#
@app.route('/backtest', methods=["POST"])
@cross_origin()
def runBacktest():
	data = request.get_json()
	stock = data['stock']
	cash = 10000.00
	indicators = data['indicators']
	endDate = datetime.now()
	startDate = endDate - dateutil.relativedelta.relativedelta(weeks=data['length'])
	# get results
	results = backtest.RunBacktest.main(stock, indicators, startDate, endDate, cash)
	# return results
	return results


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