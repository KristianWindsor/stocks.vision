import pymysql
import os
import datetime
from datetime import datetime, timedelta
import dateutil.relativedelta
import requests
import json


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


def normalizeData(n, numberList):
	return (n - min(numberList)) / (max(numberList) - min(numberList)) * 100


def closestDate(givenDate, dateList):
	returnDate = None
	for d in dateList:
		if d <= givenDate:
			if returnDate == None or d > returnDate:
				returnDate = d
	return returnDate


def main(stock, date):
	db = pymysql.connect(
		host=os.environ['MYSQL_HOSTNAME'],
		user='backend',
		passwd='pass',
		db='stocksvision',
		autocommit=True
	)
	cursor = db.cursor(pymysql.cursors.DictCursor)
	# get data
	date = datetime.strptime(date, '%Y-%m-%d').date()
	startDate = date - dateutil.relativedelta.relativedelta(weeks=2)
	sql = "SELECT * FROM stock_data WHERE ticker = '" + stock + "' AND date >= '" + startDate.strftime('%Y-%m-%d') + "' AND date <= '" + date.strftime('%Y-%m-%d') + "'"
	cursor.execute(sql)
	rows = cursor.fetchall()
	volume = None
	result = 0
	numberList = []
	dateList = []
	for row in rows:
		v = row['volume']
		d = row['date']
		numberList.append(v)
		dateList.append(d)
	
	date = closestDate(date, dateList)
	if date:
		for row in rows:
			if row['date'] == date:
				volume = row['volume']
		returnNum = normalizeData(volume, numberList)
		return returnNum
	else:
		print('[WARNING][Volume] couldn\'t find matching volume for ' + date.strftime('%Y-%m-%d'))
		return '0'

			