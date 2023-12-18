export DJANGO_SETTINGS_MODULE=site_market.settings
python manage.py collectstatic --noinput
echo 'Applying migrations...'
python manage.py migrate

gunicorn site_market.wsgi:application --bind 0.0.0.0:$PORT