#!/usr/bin/python
from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker
import os
try:
	import pymysql
	pymysql.install_as_MySQLdb()
except:
	pass
import requests
import ftplib
# tables
from database import Stocks


mysqlCreds = 'mysql://phpmyadmin:pass@' + os.environ['MYSQL_HOSTNAME'] + ':3306/stocksvision'
engine = create_engine(mysqlCreds, convert_unicode=True)
 

def main():
	dbSession = scoped_session(sessionmaker(autocommit=True, autoflush=False, bind=engine))

	filename = 'nasdaqlisted.txt'
	ftp = ftplib.FTP("ftp.nasdaqtrader.com")
	ftp.login()
	ftp.cwd("/SymbolDirectory")
	ftp.retrbinary("RETR " + filename, open(filename, 'wb').write)
	# read lines
	with open(filename) as fp:  
		line = fp.readline()
		cnt = 1
		while line:
			stockData = line.strip().split('|')
			# if line is valid
			if stockData[6] == 'Y' or stockData[6] == 'N':
				ticker = stockData[0]
				name = stockData[1]
				etf = stockData[6]
				# if row not exists
				exists = dbSession.query(
					dbSession.query(Stocks).filter_by(ticker=ticker).exists()
				).scalar()
				if not exists:
					# add the row
					newStockData = Stocks(ticker=ticker, name=name, etf=etf)
					dbSession.add(newStockData)
			line = fp.readline()
			cnt += 1
	os.remove(filename)
	dbSession.flush()