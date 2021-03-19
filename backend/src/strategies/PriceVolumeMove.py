import pymysql
import os
import datetime
from datetime import datetime, timedelta
import dateutil.relativedelta
import requests
import json
from decimal import Decimal
from strategies import VolumeUp


def max(numbers):
	highest = None
	for n in numbers:
		if highest == None:
			highest = n
		elif n > highest:
			highest = n
	return highest


def min(numbers):
	lowest = None
	for n in numbers:
		if lowest == None:
			lowest = n
		elif n < lowest:
			lowest = n
	return lowest


def normalize(n, numberList):
	return Decimal((n - min(numberList)) / (max(numberList) - min(numberList)) * (100 - -100) + -100)


def closestDate(givenDate, dateList):
	returnDate = None
	for d in dateList:
		if d <= givenDate.date():
			if returnDate == None or d > returnDate:
				returnDate = d
	return returnDate


def main(stock, givenDate):
	db = pymysql.connect(
		host=os.environ['MYSQL_HOSTNAME'],
		user='backend',
		passwd='pass',
		db='stocksvision',
		autocommit=True
	)
	cursor = db.cursor(pymysql.cursors.DictCursor)
	givenDate = datetime.strptime(givenDate, "%Y-%m-%d")
	startDate = givenDate - dateutil.relativedelta.relativedelta(weeks=2)
	# get data
	sql = "SELECT * FROM stock_data WHERE ticker = '" + stock + "' AND date >= '" + startDate.strftime('%Y-%m-%d') + "' AND date <= '" + givenDate.strftime('%Y-%m-%d') + "'"
	print(sql)
	cursor.execute(sql)
	rows = cursor.fetchall()
	lastPriceDifference = None
	priceJumpList = []
	dateList = []
	priceVolumeMap = {}
	result = 0
	for row in rows:
		priceDifference = row['close_price'] - row['open_price']
		if lastPriceDifference:
			priceJump = abs(priceDifference)
			positiveDirection = priceDifference >= 0
			priceVolumeMap[row['date'].strftime('%Y-%m-%d')] = {
				'priceJump': priceJump,
				'positiveDirection': positiveDirection
			}
			priceJumpList.append(priceJump)
			dateList.append(row['date'])
		lastPriceDifference = priceDifference

	date = closestDate(givenDate, dateList)
	priceJump = priceVolumeMap[date.strftime('%Y-%m-%d')]['priceJump']
	positiveDirection = priceVolumeMap[date.strftime('%Y-%m-%d')]['positiveDirection']
	volumeResult = Decimal(VolumeUp.main(stock, date.strftime('%Y-%m-%d')))
	priceResult = normalize(priceJump, priceJumpList)
	try:
		result = volumeResult * priceResult / 100
		print(result)
		if not positiveDirection:
			result = result * -1
		# print('\nshares ('+str(int(volumeResult))+'%) and price is up ' + str(priceJump) + ' ('+str(int(priceResult))+'%) (positive: '+str(positiveDirection)+'), so the move is ' + str(result) + '\n')
		return str(result)
	except:
		print('[WARNING][Volume] couldn\'t find matching volume for ' + givenDate.strftime('%Y-%m-%d'))
		return '0'