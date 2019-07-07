#!/usr/bin/python
import os
import pymysql
from datetime import date, timedelta


db = pymysql.connect(
	host=os.environ['MYSQL_HOSTNAME'],
	user='backend',
	passwd='pass',
	db='stocksvision',
	autocommit=True
)
cursor = db.cursor(pymysql.cursors.DictCursor)


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

	# run simulation
	portfolio = { 'cash': cash }
	portfolioNetWorth = cash
	for i in range(delta.days + 1):
		date = (startDate + timedelta(days=i))
		if date.weekday() < 5:
			print(date.strftime('%Y-%m-%d'))
			portfolioNetWorth += 5
			for indicator in indicators:
				print('indicator:' + indicator)
				stockPrice = 204.23
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
			portfolioNetWorth = portfolio['cash']
			for asset in portfolio:
				if asset != 'cash':
					portfolioNetWorth += int(portfolioNetWorth) + (int(portfolio[asset]) * int(stockPrice))
			results['chartData'][date.strftime('%Y-%m-%d')] = portfolioNetWorth

	return results

