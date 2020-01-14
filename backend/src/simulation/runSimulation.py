#!/usr/bin/python
import os
import pymysql
from datetime import datetime, date, timedelta
import indicators
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
	givenDate = datetime.date(givenDate)
	for d in dateList:
		# print(datetime.strptime(givenDate, '%Y-%m-%d'))
		# print(datetime.strptime(d, '%Y-%m-%d'))
		if d <= givenDate:
			if returnDate == None or d > returnDate:
				returnDate = d
	return returnDate


def getStockPrice(ticker, date):
	theClosestDate = closestDate(date, stockPrices[ticker])
	stockPrice = stockPrices[ticker][theClosestDate]
	return float(stockPrice)


def main(stock, indicatorSettings, startDate, endDate, cash):
	db = pymysql.connect(
		host=os.environ['MYSQL_HOSTNAME'],
		user='backend',
		passwd='pass',
		db='stocksvision',
		autocommit=True
	)
	cursor = db.cursor(pymysql.cursors.DictCursor)
	
	results = {
		'indicators': indicatorSettings,
		'chartData': {},
		'transactions': [],
		'gain': 0
	}
	print(stock)
	print(indicatorSettings)
	print(startDate)
	print(endDate)
	print(cash)

	delta = endDate - startDate

	# get stock prices
	cursor.execute("SELECT close_price, date FROM stock_data WHERE ticker = '" + stock + "' AND date >= '" + startDate.strftime('%Y-%m-%d') + "' AND date <= '" + endDate.strftime('%Y-%m-%d') + "'")
	stockPrices[stock] = {}
	for row in cursor.fetchall():
		stockPrices[stock][row['date']] = row['close_price']

	# get average indicator value
	indicatorChartData = {}
	averageIndicatorValues = {}
	print('\n\n\n')
	for i in range(delta.days + 1):
		print(i)
		print(startDate)
		date = (startDate + timedelta(days=i))
		print(date)
		if date.weekday() < 5 and date in stockPrices[stock]:
			print(date)
			indicatorData = getIndicatorValues(stock, indicatorSettings, date, cash)
			indicatorChartData[date] = indicatorData['indicatorChartData']
			averageIndicatorValues[date] = indicatorData['averageIndicatorValue']
	print('\n\n\n')
	
	# run simulation
	print(averageIndicatorValues)
	print(indicatorChartData)
	startStockPrice = getStockPrice(stock, startDate)
	portfolio = { 'cash': cash }
	if stock not in portfolio:
		portfolio[stock] = {
			'shares': float(0)	,
			'shorting': []
		}
	
	for date in averageIndicatorValues:
		# print(stockPrices)
		stockPrice = float(stockPrices[stock][date])
		fundsAllocated = portfolio['cash'] + (stockPrice * portfolio[stock]['shares'])
		for shortedPrice in portfolio[stock]['shorting']:
			fundsAllocated -= stockPrice
			fundsAllocated += shortedPrice
		quantityPossible = int(fundsAllocated / stockPrice)
		quantityShouldHave = int(quantityPossible * averageIndicatorValues[date])
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
		results['chartData'][date] =  {
			'portfolioNetWorth': portfolioNetWorth(portfolio, date),
			'portfolioNetWorthPercent': percentDifference(cash, portfolioNetWorth(portfolio, date)),
			'stockPrice': stockPrice,
			'stockPricePercent': stockPrice / startStockPrice * 100 - 100,
			'stockQuantity': portfolio[stock]['shares'] - len(portfolio[stock]['shorting']),
			'indicators': indicatorChartData[date]
		}
		
	#
	firstDate = None
	lastDate = None
	for date in results['chartData']:
		if firstDate == None or date < firstDate:
			firstDate = date
		if lastDate == None or date > lastDate:
			lastDate = date
	print(results['chartData'])
	print(lastDate)
	results['gain'] = results['chartData'][lastDate]['portfolioNetWorthPercent']
	
	print(stockPrices)
	return results


@cel.task
def getIndicatorValues(stock, indicatorSettings, date, cash):
	averageIndicatorValue = 0
	numerator = 0
	denominator = 0
	indicatorChartData = {}
	for indicatorName in indicatorSettings:
		indicatorValue = float(getattr(indicators, indicatorName).main(stock, date))
		weight = indicatorSettings[indicatorName]
		numerator += indicatorValue * weight
		denominator += abs(weight)
		indicatorChartData[indicatorName] = indicatorValue * weight
	if denominator != 0:
		averageIndicatorValue = (numerator / denominator) * 0.01 
	return {
		'averageIndicatorValue': averageIndicatorValue,
		'indicatorChartData': indicatorChartData
	}
