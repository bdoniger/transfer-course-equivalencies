release: python manage.py migrate
web: gunicorn --pythonpath="$PWD/your_app_name" config.wsgi:application
worker: python your_app_name/manage.py rqworker high default low
