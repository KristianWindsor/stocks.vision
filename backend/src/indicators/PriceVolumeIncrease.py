import pymysql
import os
import datetime
from datetime import datetime, timedelta
import dateutil.relativedelta
import requests
import json


def main(stock, date):
	db = pymysql.connect(
		host=os.environ['MYSQL_HOSTNAME'],
		user='backend',
		passwd='pass',
		db='stocksvision',
		autocommit=True
	)
	cursor = db.cursor(pymysql.cursors.DictCursor)
	startDate = datetime.strptime(date, "%Y-%m-%d")
	startDate = startDate - dateutil.relativedelta.relativedelta(days=1)
	startDate = startDate.strftime('%Y-%m-%d')
	# crawler
	rowCount = cursor.execute("SELECT id FROM stock_data WHERE ticker = '"+stock+"' AND date <= '" + startDate + "' LIMIT 1")
	if rowCount == 0:
		url = os.environ['CRAWLER_URL'] + '/runScript'
		data = json.dumps({
			"crawlerName": "StockData",
			"startDate": "2019-01-15",
			"stockTicker": stock,
			"token": "hello"
		})
		headers = { "Content-Type":"application/json" }
		res = requests.post(url, data=data, headers=headers)
		print(res.text)
	# get data
	cursor.execute("SELECT * FROM stock_data WHERE ticker = '" + stock + "' AND date >= '" + startDate + "' AND date <= '" + date + "'")
	rows = cursor.fetchall()
	lastPriceDifference = None
	lastVolume = None
	result = 0
	for row in rows:
		priceDifference = row['close_price'] - row['open_price']
		volume = row['volume']
		if lastPriceDifference and lastVolume:
			if volume > lastVolume and priceDifference > 0:
				result = 100
			elif volume > lastVolume and priceDifference < 0:
				result = -100
		lastPriceDifference = priceDifference
		lastVolume = volume
	return str(result)
