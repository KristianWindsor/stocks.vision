#!/bin/bash
set -x

# wait for mysql
until [ -n "$mysqlIsRunning" ]
do
	if [[ $(telnet $MYSQL_HOSTNAME 3306) == *"Connected to $MYSQL_HOSTNAME."* ]]
	then
		mysqlIsRunning="mysqlIsRunning"
	fi
	sleep 5
done

# update database
python3 database.py

# run flask server
python3 app.py