#!/usr/bin/python
import os
import pymysql
from datetime import date, timedelta
import indicators


db = pymysql.connect(
	host=os.environ['MYSQL_HOSTNAME'],
	user='backend',
	passwd='pass',
	db='stocksvision',
	autocommit=True
)
cursor = db.cursor(pymysql.cursors.DictCursor)

stockPrices = {}


def portfolioNetWorth(portfolio):
	netWorth = portfolio['cash']
	for ticker in portfolio:
		if ticker != 'cash':
			quantity = float(portfolio[ticker])
			price = float(stockPrices[ticker][max(stockPrices['AAPL'])])
			netWorth += quantity * price
	return netWorth


def main(stock, indicators, startDate, endDate, cash):
	results = {
		'indicators': indicators,
		'chartData': {},
		'transactions': []
	}
	print(stock)
	print(indicators)
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
	for i in range(delta.days + 1):
		date = (startDate + timedelta(days=i))
		if date.weekday() < 5 and date.strftime('%Y-%m-%d') in stockPrices[stock]:
			print(date.strftime('%Y-%m-%d'))
			portfolio['cash'] += 5
			for indicator in indicators:
				print('indicator:' + indicator)
				stockPrice = float(stockPrices[stock][date.strftime('%Y-%m-%d')])
				indicatorValue = 7
				if stockPrice < (portfolio['cash'] * indicatorValue * 0.01):
					if stock not in portfolio:
						portfolio[stock] = 0
					quantity = 2
					transaction = {
						'date': date.strftime('%Y-%m-%d'),
						'move': 'BUY',
						'stock': stock,
						'quantity': quantity,
						'price': stockPrice
					}
					portfolio[stock] += quantity
					portfolio['cash'] -= stockPrice * quantity
					results['transactions'].append(transaction)
			print(portfolio)
			results['chartData'][date.strftime('%Y-%m-%d')] = portfolioNetWorth(portfolio)

	return results

