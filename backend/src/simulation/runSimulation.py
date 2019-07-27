#!/usr/bin/python
import os
import pymysql
from datetime import datetime, date, timedelta
import indicators


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
	return ((no1 - no2) / ((no1 + no2) / 2 )) * 100 * (-1)


def closestDate(givenDate, dateList):
	returnDate = None
	for d in dateList:
		d = datetime.strptime(d, '%Y-%m-%d')
		if d < givenDate:
			if returnDate == None or d > returnDate:
				returnDate = d
	return returnDate


def getStockPrice(ticker, date):
	return float(stockPrices[ticker][closestDate(date, stockPrices[ticker]).strftime('%Y-%m-%d')])


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
		stockPrices[stock][row['date'].strftime('%Y-%m-%d')] = row['close_price']

	# run simulation
	portfolio = { 'cash': cash }
	startStockPrice = None
	for i in range(delta.days + 1):
		date = (startDate + timedelta(days=i))
		if date.weekday() < 5 and date.strftime('%Y-%m-%d') in stockPrices[stock]:
			# get indicator values
			averageIndicatorValue = 0
			numerator = 0
			denominator = 0
			indicatorChartData = {}
			if stock not in portfolio:
				portfolio[stock] = {
					'shares': 0,
					'shorting': []
				}
			#
			stockPrice = float(getStockPrice(stock, date))
			if not startStockPrice:
				startStockPrice = stockPrice
			for indicatorName in indicatorSettings:
				indicatorValue = float(getattr(indicators, indicatorName).main(stock, date.strftime('%Y-%m-%d')))
				weight = indicatorSettings[indicatorName]
				numerator += indicatorValue * weight
				denominator += abs(weight)
				indicatorChartData[indicatorName] = indicatorValue * weight
			if denominator != 0:
				averageIndicatorValue = (numerator / denominator) * 0.01 
				# buy / sell
			fundsAllocated = portfolio['cash'] + (stockPrice * portfolio[stock]['shares'])
			for shortedPrice in portfolio[stock]['shorting']:
				fundsAllocated -= stockPrice
				fundsAllocated += shortedPrice
			quantityPossible = int(fundsAllocated / stockPrice)
			quantityShouldHave = int(quantityPossible * averageIndicatorValue)
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
			#
			results['chartData'][date.strftime('%Y-%m-%d')] = {
				'portfolioNetWorth': portfolioNetWorth(portfolio, date),
				# 'portfolioNetWorthPercent': portfolioNetWorth(portfolio, date) / cash * 100 - 100,
				'portfolioNetWorthPercent': percentDifference(cash, portfolioNetWorth(portfolio, date)),
				'stockPrice': stockPrice,
				'stockPricePercent': stockPrice / startStockPrice * 100 - 100,
				'stockQuantity': portfolio[stock]['shares'] - len(portfolio[stock]['shorting']),
				'indicators': indicatorChartData
			}
	results['gain'] = percentDifference(cash, portfolioNetWorth(portfolio, date))

	return results

