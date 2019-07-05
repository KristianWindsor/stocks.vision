#!/usr/bin/python
from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker
import os
import requests
import praw
from io import StringIO
import re
from datetime import datetime
from database import RedditStocksPortfolioComment, RedditStocksPortfolioValue, Stocks


mysqlCreds = 'mysql://phpmyadmin:pass@' + os.environ['MYSQL_HOSTNAME'] + ':3306/stocksvision'
engine = create_engine(mysqlCreds, convert_unicode=True)
reddit = praw.Reddit(client_id=os.environ['REDDIT_CLIENTID'], client_secret=os.environ['REDDIT_SECRET'], user_agent='test script', password=os.environ['REDDIT_PASSWORD'], usernanme=os.environ['REDDIT_USERNAME'])


def normalizePortfolio(portfolio):
	totalSum = 0
	for ticker in portfolio:
		totalSum += float(portfolio[ticker])
	for ticker in portfolio:
		adjustedPercentage = (float(portfolio[ticker]) / totalSum) * 100
		portfolio[ticker] = adjustedPercentage
	return portfolio


def main():
	dbSession = scoped_session(sessionmaker(autocommit=True, autoflush=False, bind=engine))
	
	# Get stocks
	stockList = Stocks.query.all()
	stockTickerList = []
	stockNameList = []
	for stock in stockList:
		stockTickerList.append(stock.ticker)
		stockNameList.append(stock.name)

	# Get reddit submissions
	for submission in reddit.subreddit('stocks').search('Rate My Portfolio - r/Stocks Quarterly Thread'):
		print(submission.title)
		# Get reddit comments
		submission.comments.replace_more(limit=None, threshold=0)
		for comment in submission.comments.list():
			if comment.body.count('%') > 2:
				portfolio = {}
				s = StringIO(comment.body)
				# print(s)
				for line in s:
					if line.count('%') == 1:
						percentage = None
						ticker = None
						# iterate over each word
						for word in line.split(' '):
							if word.count('%') == 1:
								percentage = re.sub(r'[^\d.]+', '', word)
							if word in stockTickerList:
								ticker = word
						# next try looking for company name
						if ticker == None:
							for stockName in stockNameList:
								if stockName.replace(', Inc.', '').replace(' Inc.', '') in line:
									index = stockNameList.index(stockName)
									ticker = stockTickerList[index]
						# save values
						if ticker != None and percentage != None:
							try:
								portfolio[ticker] = float(percentage)
							except ValueError:
								pass
				if portfolio == {}:
					print('fail!')
				else:
					if comment.author:
						portfolio = normalizePortfolio(portfolio)
						reddit_id = str(comment.id)
						user = str(comment.author)
						karma = int(comment.ups - comment.downs)
						date = datetime.utcfromtimestamp(comment.created).strftime('%Y-%m-%d')
						#
						exists = dbSession.query(
							dbSession.query(RedditStocksPortfolioComment).filter_by(reddit_id=reddit_id).exists()
						).scalar()
						if not exists:
							newCommentRow = RedditStocksPortfolioComment(reddit_id=reddit_id, user=user, karma=karma, date=date)
							dbSession.add(newCommentRow)
							dbSession.flush()
							for ticker in portfolio:
								newPortfolioValueRow = RedditStocksPortfolioValue(comment_id=newCommentRow.id, ticker=ticker, percent=portfolio[ticker])
								dbSession.add(newPortfolioValueRow)
	dbSession.flush()
	dbSession.close()

