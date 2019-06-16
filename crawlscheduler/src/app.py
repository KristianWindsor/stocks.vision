#!/usr/bin/python
import requests
import json
import time
import os

header = {
	"Content-Type":"application/json"
}
data = {
	"crawlerName": "StockData",
	"startDate": "2019-01-15",
	"token": "hello"
}
url = 'http://' + os.environ['CRAWLAPI_HOSTNAME'] + ':8083/runScript'
res = requests.post(url, data=json.dumps(data), headers=header)

print(res.text)

while True:
	time.sleep(1)