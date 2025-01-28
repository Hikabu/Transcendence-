#!/bin/bash

# Wait for database
echo "Waiting for database..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
done
echo "Database started"

# Run migrations
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Start Daphne
exec daphne -b 0.0.0.0 -p 8000 project.asgi:application