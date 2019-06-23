#!/usr/bin/python
import requests
import json
import time
import os
import pymysql


# get list of all stocks
# check if the data is there
def crawlapi(data):
	headers = { "Content-Type":"application/json" }
	url = 'http://' + os.environ['CRAWLAPI_HOSTNAME'] + ':8083/runScript'
	res = requests.post(url, data=json.dumps(data), headers=headers)
	print(res.text)


db = pymysql.connect(
	host='db',
	user='phpmyadmin',
	passwd='pass',
	db='stocksvision',
	autocommit=True
)
cursor = db.cursor(pymysql.cursors.DictCursor)



crawlapi({
	"crawlerName": "Stocks",
	"token": "hello"
})


listOfAllStocks = cursor.execute("SELECT ticker FROM stocks")
for row in cursor.fetchall():
	stockTicker = row['ticker']
	print('StockData: ' + stockTicker)
	crawlapi({
		"crawlerName": "StockData",
		"startDate": "2019-01-15",
		"stockTicker": stockTicker,
		"token": "hello"
	})
	time.sleep(2)


while True:
	time.sleep(1)