#!/usr/bin/python
import requests
import json
import time
import os



# get list of all stocks
# check if the data is there
# maybe get the data everytime or use a cronjob
# if the data is not there, tell crawlapi to get it
# once the data is there, put it into a local variable

# get data on each stock
# loop over that motherfackin list
header = {
	"Content-Type":"application/json"
}
data = {
	"crawlerName": "StockData",
	"startDate": "2019-01-15",
	"stockTicker": "AAPL",
	"token": "hello"
}
url = 'http://' + os.environ['CRAWLAPI_HOSTNAME'] + ':8083/runScript'
res = requests.post(url, data=json.dumps(data), headers=header)

print(res.text)

while True:
	time.sleep(1)