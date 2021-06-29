#!/bin/bash

set -m 	

if [$CONTAINER_TYPE = "backend"]
then 
	echo --- backend --- 
	exec python manage.py runserver

elif [$CONTAINER_TYPE = "scheduler"]
then	
	echo --- scheduler --- 
	exec python manage.py rqscheduler

elif [$CONTAINER_TYPE = "worker"]
then
	echo --- worker --- 
	exec python manage.py rqworker

else
	echo unknow $CONTAINER_TYPE
fi