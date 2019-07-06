#!/usr/bin/python
import os
import pymysql


db = pymysql.connect(
	host=os.environ['MYSQL_HOSTNAME'],
	user='backend',
	passwd='pass',
	db='stocksvision',
	autocommit=True
)
cursor = db.cursor(pymysql.cursors.DictCursor)


def main(stock, indicators, startDate, endDate, cash):
	results = {
		'indicators': {},
		'chartData': {},
		'transactions': []
	}
	print(stock)
	print(indicators)
	print(startDate)
	print(endDate)
	print(cash)
	# run simulation
	for indicator in indicators:
		print('indicator:' + indicator)

	return results

