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
if [ "$USE_GUNICORN" == "true" ]
then
	gunicorn --workers 10 --timeout 300 --bind 0.0.0.0:5000 wsgi
else
	python3 app.py
fi