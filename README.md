# Stocks.Vision
Stock trading bot and information aggregator

# View it live

This project is currently live at https://stocks.vision

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

View the database: http://localhost:8080/

View the UI: http://localhost/


# Microservice architecture

WebUI - visualizes data analyzed by the backend

Backend - analyzes data from the database

MySQL - the database

Crawler - collects data from external sources and inserts it into the database

CrawlScheduler - triggers the crawler scripts at certain time intervals

# Crawlers

A crawler is a script that collects data from any source on the Internet. Most of these are public APIs, such as [Alpha Vantage](https://www.alphavantage.co/documentation/) or [Reddit](https://www.reddit.com/dev/api/).

Each of these will insert content into the database. You can see the data through phpMyAdmin at https://localhost:8080

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

First you need to create a Reddit app (script for personal use): https://www.reddit.com/prefs/apps/

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

# Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

# License

[MIT License](https://github.com/KristianWindsor/stocks.vision/blob/master/LICENSE.md)