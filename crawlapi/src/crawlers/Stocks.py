#!/usr/bin/python
from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker
import os
import requests
import ftplib
from database import Stocks


mysqlCreds = 'mysql://phpmyadmin:pass@' + os.environ['MYSQL_HOSTNAME'] + ':3306/stocksvision'
engine = create_engine(mysqlCreds, convert_unicode=True)

def getFileAndParseData(dbSession, ftp, filename):
	ftp.retrbinary("RETR " + filename, open(filename, 'wb').write)
	with open(filename) as fp:  
		line = fp.readline()
		legend = line.strip().split('|')
		if 'nasdaq' in filename:
			indexTicker = legend.index('Symbol')
		else:
			indexTicker = legend.index('NASDAQ Symbol')
		indexName = legend.index('Security Name')
		indexETF = legend.index('ETF')
		while line:
			line = fp.readline()
			stockData = line.strip().split('|')
			# if line is valid
			if len(stockData) == 8 and (stockData[indexETF] == 'Y' or stockData[indexETF] == 'N'):
				ticker = stockData[indexTicker]
				name = stockData[indexName]
				etf = int(stockData[indexETF].replace('N','0').replace('Y','1'))
				if ' - ' in name:
					name = name.split(' - ')[0]
				if ', ' in name:
					name = name.split(', ')[0]
				# if row not exists
				exists = dbSession.query(
					dbSession.query(Stocks).filter_by(ticker=ticker).exists()
				).scalar()
				if not exists:
					# add the row
					newStockData = Stocks(ticker=ticker, name=name, etf=etf)
					dbSession.add(newStockData)
			else:
				print('oops')
	os.remove(filename)

def main():
	dbSession = scoped_session(sessionmaker(autocommit=True, autoflush=False, bind=engine))

	ftp = ftplib.FTP("ftp.nasdaqtrader.com")
	ftp.login()
	ftp.cwd("/SymbolDirectory")

	getFileAndParseData(dbSession, ftp, 'nasdaqlisted.txt')
	getFileAndParseData(dbSession, ftp, 'otherlisted.txt')

	dbSession.flush()
	dbSession.close()