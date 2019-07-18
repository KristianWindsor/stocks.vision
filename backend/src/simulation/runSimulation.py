#!/usr/bin/python
import os
import pymysql
from datetime import date, timedelta
import indicators


stockPrices = {}


def portfolioNetWorth(portfolio, date):
	netWorth = portfolio['cash']
	for ticker in portfolio:
		if ticker != 'cash':
			quantity = float(portfolio[ticker])
			price = float(stockPrices[ticker][date.strftime('%Y-%m-%d')])
			netWorth += quantity * price
	return netWorth


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
		'transactions': []
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
	print(stockPrices)

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
			stockPrice = float(stockPrices[stock][date.strftime('%Y-%m-%d')])
			if not startStockPrice:
				startStockPrice = stockPrice
			for indicatorName in indicatorSettings:
				indicatorValue = float(getattr(indicators, indicatorName).main(stock, date.strftime('%Y-%m-%d')))
				indicatorChartData[indicatorName] = indicatorValue
				weight = indicatorSettings[indicatorName]
				numerator += indicatorValue * weight
				denominator += weight
			if denominator != 0:
				averageIndicatorValue = numerator / denominator
			# do math
			if averageIndicatorValue >= 0:
				fundsAllocated = portfolio['cash'] * averageIndicatorValue * 0.01
			else:
				fundsAllocated = (portfolio['cash'] + (stockPrice * portfolio[stock])) * averageIndicatorValue * 0.01
			if abs(fundsAllocated) > stockPrice:
				# buy / sell
				quantity = int(fundsAllocated / stockPrice)
				if quantity > 0:
					action = 'BUY'
					portfolio[stock] += quantity
					portfolio['cash'] -= stockPrice * quantity
				elif quantity < 0:
					action = 'SELL'
					portfolio[stock] += quantity
					portfolio['cash'] -= stockPrice * quantity
				results['transactions'].append({
					'date': date.strftime('%Y-%m-%d'),
					'move': action,
					'stock': stock,
					'quantity': quantity,
					'price': stockPrice
				})
			print(portfolio)
			results['chartData'][date.strftime('%Y-%m-%d')] = {
				'portfolioNetWorth': portfolioNetWorth(portfolio, date),
				'portfolioNetWorthPercent': portfolioNetWorth(portfolio, date) / cash * 100 - 100,
				'stockPrice': stockPrice,
				'stockPricePercent': stockPrice / startStockPrice * 100 - 100,
				'stockQuantity': portfolio[stock],
				'indicators': indicatorChartData
			}


	return results

