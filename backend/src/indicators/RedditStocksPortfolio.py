#!/usr/bin/python
import os
import pymysql
from datetime import datetime, timedelta
import dateutil.relativedelta
import decimal
import time
import json


db = pymysql.connect(
	host=os.environ['MYSQL_HOSTNAME'],
	user='backend',
	passwd='pass',
	db='stocksvision',
	autocommit=True
)
cursor = db.cursor(pymysql.cursors.DictCursor)


def main(stock, date):
	# get average portfolio
	startDate = datetime.strptime(date, "%Y-%m-%d")
	startDate = startDate - dateutil.relativedelta.relativedelta(months=1)
	startDate = startDate.strftime('%Y-%m-%d')
	print(startDate)
	print(date)
	cursor.execute("SELECT id, karma FROM reddit_stocks_portfolio_comment WHERE date >= '" + startDate + "' AND date <= '" + date + "'")
	comments = cursor.fetchall()
	averagePortfolio = {}
	count = 0
	for comment in comments:
		sql = "SELECT ticker, percent FROM reddit_stocks_portfolio_value WHERE comment_id='" + str(comment['id']) + "'"
		cursor.execute(sql)
		allValues = cursor.fetchall()
		for v in allValues:
			increase = v['percent'] * decimal.Decimal((comment['karma'] + 1) / 2)
			if v['ticker'] not in averagePortfolio:
				averagePortfolio[v['ticker']] = increase
			else:
				averagePortfolio[v['ticker']] += increase
		count += 1
	if stock in averagePortfolio:
		# find scale ratio
		biggestPercent = 0
		for t in averagePortfolio:
			p = averagePortfolio[t] / count
			if p > biggestPercent:
				biggestPercent = p
		scaleRatio = 100 / biggestPercent
		# return value
		returnValue = (averagePortfolio[stock] / count) * scaleRatio
		return str(returnValue)
	else:
		return '0'