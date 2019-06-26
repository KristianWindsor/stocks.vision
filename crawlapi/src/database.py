from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import os
try:
	import pymysql
	pymysql.install_as_MySQLdb()
except:
	pass
 

Base = declarative_base()
mysqlCreds = 'mysql://phpmyadmin:pass@' + os.environ['MYSQL_HOSTNAME'] + ':3306/stocksvision'




class Stocks(Base):
	__tablename__ = 'stocks'
	ticker = Column(String(5), primary_key=True)
	name = Column(String(200)) # should find character limit
	etf = Column(String(1)) # should be boolean

class StockData(Base):
	__tablename__ = 'stock_data'
	id = Column(Integer(), primary_key=True)
	ticker = Column(String(5), nullable=False)
	date = Column(Date(), nullable=False)
	open_price = Column(Numeric(11,4))
	high_price = Column(Numeric(11,4))
	low_price = Column(Numeric(11,4))
	close_price = Column(Numeric(11,4))
	volume = Column(Integer())

class RedditStocksPortfolioComment(Base):
	__tablename__ = 'reddit_stocks_portfolio_comment'
	id = Column(Integer(), primary_key=True)
	user = Column(String(40))
	karma = Column(Integer())
	date = Column(Date(), nullable=False)

class RedditStocksPortfolioValue(Base):
	__tablename__ = 'reddit_stocks_portfolio_value'
	comment_id = Column(Integer(), primary_key=True)
	ticker = Column(String(5), nullable=False)
	percent = Column(Numeric(11,4))
 



engine = create_engine(mysqlCreds, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base.query = db_session.query_property()
Base.metadata.create_all(bind=engine)
