#!/usr/bin/python
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import os
try:
	import pymysql
	pymysql.install_as_MySQLdb()
except:
	pass
# tables
from database import StockData


mysqlCreds = 'mysql://phpmyadmin:pass@' + os.environ['MYSQL_HOSTNAME'] + ':3306/stocksvision'
engine = create_engine(mysqlCreds, convert_unicode=True)
 

def main():
	db_session = scoped_session(sessionmaker(autocommit=True, autoflush=False, bind=engine))

	newStockData = StockData(ticker='TSLA', date='2019-06-12')
	db_session.add(newStockData)

	db_session.flush()