#!/usr/bin/python
import requests
import json
import time
import os
import pymysql

# connect to mysql
for i in range(100):
	for attempt in range(5):
		try:
			db = pymysql.connect(
				host=os.environ['MYSQL_HOSTNAME'],
				user='crawlscheduler',
				passwd='pass',
				db='stocksvision',
				autocommit=True
			)
			cursor = db.cursor(pymysql.cursors.DictCursor)
		except:
			time.sleep(1)
		else:
			break
	else:
		print('Trying to connect to MySQL...')

#
# crawlapi function
#
def crawlapi(data):
	headers = { "Content-Type":"application/json" }
	url = 'http://' + os.environ['CRAWLAPI_HOSTNAME'] + ':8083/runScript'
	res = requests.post(url, data=json.dumps(data), headers=headers)
	print(res.text)


# Stock Data
def getAllStockData():
	listOfAllStocks = cursor.execute("SELECT ticker FROM stocks")
	for row in cursor.fetchall():
		stockTicker = row['ticker']
		doesDataAlreadyExist = cursor.execute('SELECT * FROM stock_data WHERE ticker = "' + stockTicker + '"')
		if doesDataAlreadyExist == 0:
			print('StockData: ' + stockTicker)
			crawlapi({
				"crawlerName": "StockData",
				"startDate": "2019-01-15",
				"stockTicker": stockTicker,
				"token": "hello"
			})
			time.sleep(5)


# keep container alive
while True:
	time.sleep(1)