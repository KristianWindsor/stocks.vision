#!/usr/bin/python
from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker
import os
import requests
from database import StockData


mysqlCreds = 'mysql://crawler:pass@' + os.environ['MYSQL_HOSTNAME'] + ':3306/stocksvision'
engine = create_engine(mysqlCreds, convert_unicode=True)
 

def main(startDate, stockTicker):
	dbSession = scoped_session(sessionmaker(autocommit=True, autoflush=False, bind=engine))

	alphavantageURL = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+stockTicker+'&outputsize=full&apikey=0SV1D44TD1QQXIZK'
	theData = requests.get(alphavantageURL).json()
	if "Error Message" in theData:
		print("shit." + theData["Error Message"])
	elif "Time Series (Daily)" in theData:
		for majorkey, subdict in theData["Time Series (Daily)"].items():
			# get values from json
			open_price = subdict['1. open']
			high_price = subdict['2. high']
			low_price = subdict['3. low']
			close_price = subdict['4. close']
			volume = subdict['5. volume']
			date = majorkey
			# if ticker & date don't match an existing row
			exists = dbSession.query(
				dbSession.query(StockData).filter_by(ticker=stockTicker, date=date).exists()
			).scalar()
			if not exists:
				# add the row
				newStockData = StockData(ticker=stockTicker, open_price=open_price, high_price=high_price, low_price=low_price, close_price=close_price, volume=volume, date=date)
				dbSession.add(newStockData)
	else:
		print('shit. ' + theData)

	dbSession.flush()
	dbSession.close()