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
	host=os.environ['MYSQL_HOSTNAME'],
	user='phpmyadmin',
	passwd='pass',
	db='stocksvision',
	autocommit=True
)
cursor = db.cursor(pymysql.cursors.DictCursor)


# Stocks
crawlapi({
	"crawlerName": "Stocks",
	"token": "hello"
})


# Reddit Stocks Portfolio
crawlapi({
	"crawlerName": "RedditStocksPortfolio",
	"token": "hello"
})


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
#getAllStockData()


while True:
	time.sleep(1)