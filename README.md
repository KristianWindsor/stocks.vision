# Stocks Vision

Stocks Vision is a stock trading bot and information aggregator.

This project is currently live at [https://stocks.vision](https://stocks.vision/).

# Run this locally
You will need [docker desktop](https://www.docker.com/products/docker-desktop) installed.

<!-- ## Download and run -->
Clone the repo
```
git clone https://github.com/KristianWindsor/stocks.vision.git
```

Start the app
```
docker-compose up
```

View the UI: http://localhost/

View the database: http://localhost:8080/

# Microservice architecture

WebUI - visualizes data analyzed by the backend

Backend - analyzes data from the database

DB - the mysql database

Crawler - collects data from external sources and inserts it into the database

CrawlScheduler - triggers the crawler scripts at certain time intervals

# Usage: Crawlers

A crawler is a script that collects data from any source on the Internet. Most of these are public APIs, such as [Alpha Vantage](https://www.alphavantage.co/documentation/) or [Reddit](https://www.reddit.com/dev/api/).

The collected data is inserted into the database. You can view the database with any database client.

## List of stocks

Populate the database with a complete list of stock tickers and the names of the companies.

Trigger the crawl script:

```bash
curl -X POST -H "Content-Type: application/json" -d '{
    "crawlerName": "Stocks",
    "token": "hello"
}' http://localhost:5001/runScript
```

## Stock Data

Get data such as opening/closing prices, highest/lowest prices, and the volume of trades per day.

Trigger the crawl script:

```bash
curl -X POST -H "Content-Type: application/json" -d '{
    "crawlerName": "StockData",
    "stockTicker": "AAPL",
    "startDate": "2020-04-20",
    "token": "hello"
}' http://localhost:5001/runScript
```

## Reddit /r/stocks

First you need to [create a Reddit app (script for personal use)](https://www.reddit.com/prefs/apps/).

Second you need to create a `environment.env` file:

```
REDDIT_USERNAME=myusername
REDDIT_PASSWORD=mypassword
REDDIT_SECRET=myredditsecret
REDDIT_CLIENTID=myredditclientid
```

Then you can trigger the script:
```bash
curl -X POST -H "Content-Type: application/json" -d '{
    "crawlerName": "RedditStocksPortfolio",
    "token": "hello"
}' http://localhost:5001/runScript
```

## Create your own Crawler Script

A crawler is just a python script that scrapes data from somewhere and stores it into the database. 

To create your own and add it to stocks vision, do the following

1. To create a new table in the database, add it to `./crawlers/database.py` where the database is defined using SQLAlchemy.

2. Create a python script at `./crawler/src/crawlers/myscript.py`.

3. Schedule it at regular intervals by triggering it in `./crawlscheduler/src/app.py` with this script
```bash
curl -X POST -H "Content-Type: application/json" -d '{
    "crawlerName": "MyCrawler",
    "token": "hello"
}' http://localhost:5001/runScript
```

# Usage: Strategies

<!-- A is a script that collects data from any source on the Internet. Most of these are public APIs, such as [Alpha Vantage](https://www.alphavantage.co/documentation/) or [Reddit](https://www.reddit.com/dev/api/).

The collected data is inserted into the database. You can view the database through phpMyAdmin at https://localhost:8080

## List of stocks

Populate the database with a complete list of stock tickers and the names of the companies.

Trigger the crawl script:

```bash
curl -X POST -H "Content-Type: application/json" -d '{
    "crawlerName": "Stocks",
    "token": "hello"
}' http://localhost:5001/runScript
``` -->


# Contributing

<!-- This project is structured so that it is easy to write new strategies and crawlers. If you want to use a 3rd party API or collect your own data from any website or platform, Stocks Vision has an expansive range of capabilities.  -->

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

# License

[MIT License](https://github.com/KristianWindsor/stocks.vision/blob/master/LICENSE.md)