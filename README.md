# Stocks.Vision
Stock trading bot and information aggregator

# Run this locally
You will need docker desktop installed.

Create environment.env file
```
REDDIT_USERNAME=myusername
REDDIT_PASSWORD=mypassword
REDDIT_SECRET=myredditsecret
REDDIT_CLIENTID=myredditclientid
```

Start the app
```
docker-compose up
```

# Populate the database

Populate database with list of stocks
```
curl -X POST -H "Content-Type: application/json" -d '{
    "crawlerName": "Stocks",
    "token": "hello"
}' http://localhost:5001/runScript
```

Get stock data like prices and volume
```
curl -X POST -H "Content-Type: application/json" -d '{
    "crawlerName": "StockData",
    "stockTicker": "TSLA",
    "startDate": "2020-04-20",
    "token": "hello"
}' http://localhost:5001/runScript
```

Crawl Reddit /r/stocks
```
curl -X POST -H "Content-Type: application/json" -d '{
    "crawlerName": "RedditStocksPortfolio",
    "token": "hello"
}' http://localhost:5001/runScript
```