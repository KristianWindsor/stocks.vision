#!/bin/bash
set -x

# wait for mysql\
until [ -n "$mysqlIsRunning" ]
do
	if [[ $(telnet db 3306) == *"Connected to db."* ]]
	then
		mysqlIsRunning="true"
	fi
	sleep 5
done

# update database
python3 database.py

# run crawler
python3 crawler.py