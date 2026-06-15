web: python manage.py collectstatic --no-input && python manage.py migrate && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
