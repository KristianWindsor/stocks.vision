#!/usr/bin/python
from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker
import os
import requests
from database import RedditStocksPortfolioComment, RedditStocksPortfolioValue


mysqlCreds = 'mysql://phpmyadmin:pass@' + os.environ['MYSQL_HOSTNAME'] + ':3306/stocksvision'
engine = create_engine(mysqlCreds, convert_unicode=True)



def main():
	dbSession = scoped_session(sessionmaker(autocommit=True, autoflush=False, bind=engine))
	print('running reddit stocks portfolio thread crawler')

	
	
	dbSession.flush()