#!/bin/bash

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 2
  echo "Waiting postgres...."
done

celery -A config worker -l info
