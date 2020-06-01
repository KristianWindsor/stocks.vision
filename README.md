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

CrawlScheduler - triggers Crawler in a cron-like fashion

# Setup and use

## List of stocks

Populate the database with list of stocks

<!-- A complete list of stocks is needed for some operations. This curl command will trigger the crawler script to get a complete list of stocks and populate the database with the information. The actual script is at `crawler/src/crawlers/Stocks.py`. -->

```bash
curl -X POST -H "Content-Type: application/json" -d '{
    "crawlerName": "Stocks",
    "token": "hello"
}' http://localhost:5001/runScript
```
<!-- You can view the DB's table full of stocks through [phpMyAdmin](http://localhost:8080/sql.php?server=1&db=stocksvision&table=stocks).-->

## Reddit /r/stocks

Create a Reddit app (script for personal use): https://www.reddit.com/prefs/apps/

Create `environment.env` file

```
REDDIT_USERNAME=myusername
REDDIT_PASSWORD=mypassword
REDDIT_SECRET=myredditsecret
REDDIT_CLIENTID=myredditclientid
```

Trigger the script
```bash
curl -X POST -H "Content-Type: application/json" -d '{
    "crawlerName": "RedditStocksPortfolio",
    "token": "hello"
}' http://localhost:5001/runScript
```

<!--The UI will trigger the crawler to get stock data for whatever stock is entered into the text field.

To trigger it manually though, run this:
```
curl -X POST -H "Content-Type: application/json" -d '{
    "crawlerName": "StockData",
    "stockTicker": "AAPL",
    "startDate": "2020-04-20",
    "token": "hello"
}' http://localhost:5001/runScript
``` -->