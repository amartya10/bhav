#!/bin/bash

set -m 	

if [ $CONTAINER_TYPE = 'backend' ]
then 
	exec python manage.py runserver 0.0.0.0:8000

elif [ $CONTAINER_TYPE = 'scheduler' ]
then	
	exec python manage.py rqscheduler

elif [ $CONTAINER_TYPE = 'worker' ] 
then
	exec python manage.py rqworker

else
	echo unknow $CONTAINER_TYPE
fi
