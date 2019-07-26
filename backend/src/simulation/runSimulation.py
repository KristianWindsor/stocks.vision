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
			quantity = float(portfolio[ticker])
			price = float(getStockPrice(ticker, date))
			netWorth += quantity * price
	return netWorth


def percentDifference(no1, no2):
	return (abs(no1 - no2) / ((no1 + no2) / 2 )) * 100


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
			print(date.strftime('%Y-%m-%d'))
			# get indicator values
			averageIndicatorValue = 0
			numerator = 0
			denominator = 0
			indicatorChartData = {}
			if stock not in portfolio:
				portfolio[stock] = 0
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
			fundsAllocated = portfolio['cash'] + (stockPrice * portfolio[stock])
			quantityPossible = int(fundsAllocated / stockPrice)
			quantityShouldHave = int(quantityPossible * averageIndicatorValue)
			quantityToMove = quantityShouldHave - portfolio[stock]
			if quantityToMove > 0:
				action = 'BUY'
				portfolio[stock] += quantityToMove
				portfolio['cash'] -= stockPrice * quantityToMove
			elif quantityToMove < 0:
				action = 'SELL'
				portfolio[stock] += quantityToMove
				portfolio['cash'] -= stockPrice * quantityToMove
			if quantityToMove != 0:
				results['transactions'].append({
					'date': date.strftime('%Y-%m-%d'),
					'move': action,
					'stock': stock,
					'quantity': quantityToMove,
					'price': stockPrice
				})
			results['chartData'][date.strftime('%Y-%m-%d')] = {
				'portfolioNetWorth': portfolioNetWorth(portfolio, date),
				# 'portfolioNetWorthPercent': portfolioNetWorth(portfolio, date) / cash * 100 - 100,
				'portfolioNetWorthPercent': percentDifference(cash, portfolioNetWorth(portfolio, date)),
				'stockPrice': stockPrice,
				'stockPricePercent': stockPrice / startStockPrice * 100 - 100,
				'stockQuantity': portfolio[stock],
				'indicators': indicatorChartData
			}
	results['gain'] = percentDifference(cash, portfolioNetWorth(portfolio, date))

	return results

