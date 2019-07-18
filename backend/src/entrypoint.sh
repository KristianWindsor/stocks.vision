#!/bin/bash

# wait for mysql
until [ -n "$mysqlIsRunning" ]
do
	if [[ $(telnet $MYSQL_HOSTNAME 3306) == *"Connected to $MYSQL_HOSTNAME."* ]]
	then
		mysqlIsRunning="mysqlIsRunning"
	fi
	sleep 2
done

set -x

# run flask server
gunicorn --workers 10 --bind 0.0.0.0:5000 wsgi