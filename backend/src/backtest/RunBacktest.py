#!/usr/bin/python
import os, json, requests
import pymysql
from datetime import datetime, date, timedelta
import strategies
from celery import Celery

cel = Celery('celery_blog', broker='redis://localhost:6379/0')


stockPrices = {}


def portfolioNetWorth(portfolio, date):
	netWorth = portfolio['cash']
	for ticker in portfolio:
		if ticker != 'cash':
			quantity = abs(float(portfolio[ticker]['shares']))
			price = float(getStockPrice(ticker, date))
			netWorth += quantity * price
			for soldShortPrice in portfolio[ticker]['shorting']:
				netWorth -= price
				netWorth += soldShortPrice
	return netWorth


def percentDifference(no1, no2):
	diff = ((no1 - no2) / ((no1 + no2) / 2 )) * 100 * (-1)
	return diff


def closestDate(givenDate, dateList):
	returnDate = None
	for d in dateList:
		d = datetime.strptime(d, '%Y-%m-%d')
		if d <= givenDate:
			if returnDate == None or d > returnDate:
				returnDate = d
	return returnDate


def getStockPrice(ticker, date):
	try:
		# get the date we're looking for in the format we want
		dateString = closestDate(date, stockPrices[ticker]).strftime('%Y-%m-%d')
		# now get the stock price using the date as the key
		stockPrice = stockPrices[ticker][dateString]
		# return the price as a decimal number
		return float(stockPrice)
	except:
		return None


def main(stock, strategySettings, startDate, endDate, cash):
	db = pymysql.connect(
		host=os.environ['MYSQL_HOSTNAME'],
		user='backend',
		passwd='pass',
		db='stocksvision',
		autocommit=True
	)
	cursor = db.cursor(pymysql.cursors.DictCursor)
	
	results = {
		'strategies': strategySettings,
		'chartData': {},
		'transactions': [],
		'gain': 0
	}
	print(stock)
	print(strategySettings)
	print(startDate)
	print(endDate)
	print(cash)

	delta = endDate - startDate

	# make sure enough data exists
	rowCount = cursor.execute("SELECT id FROM stock_data WHERE ticker = '" + stock + "' AND date <= '" + startDate.strftime('%Y-%m-%d') + "' LIMIT 1")
	if rowCount == 0:
		print("Not enough stock data to run backtest. Calling Crawler to fetch more data.")
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

	# get stock prices
	getDataStartDate = startDate - timedelta(days=7)
	cursor.execute("SELECT close_price, date FROM stock_data WHERE ticker = '" + stock + "' AND date >= '" + getDataStartDate.strftime('%Y-%m-%d') + "' AND date <= '" + endDate.strftime('%Y-%m-%d') + "'")
	stockPrices[stock] = {}
	for row in cursor.fetchall():
		stockPrices[stock][row['date'].strftime('%Y-%m-%d')] = row['close_price']

	# get average strategy value
	strategyChartData = {}
	averageStrategyValues = {}
	for i in range(delta.days + 1):
		date = (startDate + timedelta(days=i))
		dateString = date.strftime('%Y-%m-%d')
		if date.weekday() < 5 and date.strftime(dateString) in stockPrices[stock]:
			strategyData = getStrategyValues(stock, strategySettings, date, cash)
			strategyChartData[dateString] = strategyData['strategyChartData']
			averageStrategyValues[dateString] = strategyData['averageStrategyValue']
	
	# run backtest
	print(averageStrategyValues)
	print(strategyChartData)
	startStockPrice = getStockPrice(stock, startDate)
	portfolio = { 'cash': cash }
	if stock not in portfolio:
		portfolio[stock] = {
			'shares': float(0)	,
			'shorting': []
		}
	
	for dateString in averageStrategyValues:
		date = datetime.strptime(dateString, '%Y-%m-%d')
		# print(stockPrices)
		stockPrice = float(stockPrices[stock][dateString])
		fundsAllocated = portfolio['cash'] + (stockPrice * portfolio[stock]['shares'])
		for shortedPrice in portfolio[stock]['shorting']:
			fundsAllocated -= stockPrice
			fundsAllocated += shortedPrice
		quantityPossible = int(fundsAllocated / stockPrice)
		quantityShouldHave = int(quantityPossible * averageStrategyValues[dateString])
		currentQuantity = portfolio[stock]['shares'] - len(portfolio[stock]['shorting'])
		quantityToMove = quantityShouldHave - currentQuantity
		if quantityToMove > 0:
			# bull
			while quantityToMove != 0:
				if len(portfolio[stock]['shorting']) > 0:
					# buy back short
					portfolio['cash'] -= stockPrice
					portfolio['cash'] += portfolio[stock]['shorting'][0]
					portfolio[stock]['shorting'].pop(0)
				else:
					# buy shares
					portfolio[stock]['shares'] += 1
					portfolio['cash'] -= stockPrice
				quantityToMove -= 1
		elif quantityToMove < 0:
			# bear
			while quantityToMove != 0:
				if portfolio[stock]['shares'] > 0:
					# sell shares
					portfolio[stock]['shares'] -= 1
					portfolio['cash'] += stockPrice
				else:
					# sell short
					portfolio[stock]['shorting'].append(stockPrice)
				quantityToMove += 1
		print(portfolio)
		#
		results['chartData'][date.strftime('%Y-%m-%d')] =  {
			'portfolioNetWorth': portfolioNetWorth(portfolio, date),
			'portfolioNetWorthPercent': percentDifference(cash, portfolioNetWorth(portfolio, date)),
			'stockPrice': stockPrice,
			'stockPricePercent': stockPrice / startStockPrice * 100 - 100,
			'stockQuantity': portfolio[stock]['shares'] - len(portfolio[stock]['shorting']),
			'strategies': strategyChartData[date.strftime('%Y-%m-%d')]
		}
		
	#
	firstDate = None
	lastDate = None
	for dateString in results['chartData']:
		date = datetime.strptime(dateString, '%Y-%m-%d')
		if firstDate == None or date < firstDate:
			firstDate = date
		if lastDate == None or date > lastDate:
			lastDate = date
	results['gain'] = results['chartData'][lastDate.strftime('%Y-%m-%d')]['portfolioNetWorthPercent']
	return results


@cel.task
def getStrategyValues(stock, strategySettings, date, cash):
	averageStrategyValue = 0
	numerator = 0
	denominator = 0
	strategyChartData = {}
	for strategyName in strategySettings:
		strategyValue = float(getattr(strategies, strategyName).main(stock, date.strftime('%Y-%m-%d')))
		weight = strategySettings[strategyName]
		numerator += strategyValue * weight
		denominator += abs(weight)
		strategyChartData[strategyName] = strategyValue * weight
	if denominator != 0:
		averageStrategyValue = (numerator / denominator) * 0.01 
	return {
		'averageStrategyValue': averageStrategyValue,
		'strategyChartData': strategyChartData
	}
