#!/bin/sh

echo "⏳ Waiting for database to be ready..."
/wait-for-it.sh madebayosqlserver.database.windows.net:1433 -t 60 -- echo "✅ Database is ready!"

echo "🚀 Running migrations..."
python manage.py migrate || { echo "❌ Migrations failed. Retrying..."; sleep 5; python manage.py migrate; }

echo "🔄 Starting Gunicorn..."
gunicorn MySbaApp.wsgi:application  --workers 2 --timeout 120 --bind 0.0.0.0:8000 || { echo "❌ Gunicorn failed to start"; exit 1; }