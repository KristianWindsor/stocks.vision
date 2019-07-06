#!/bin/bash

# wait for mysql
until [ -n "$mysqlIsRunning" ]
do
	if [[ $(telnet $MYSQL_HOSTNAME 3306) == *"Connected to $MYSQL_HOSTNAME."* ]]
	then
		mysqlIsRunning="mysqlIsRunning"
	fi
	sleep 5
done

set -x

# run flask server
python3 app.py