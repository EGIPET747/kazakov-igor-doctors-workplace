release: python manage.py migrate
web: gunicorn --bind 0.0.0.0:8000 TESTDJANGO.wsgi:application
