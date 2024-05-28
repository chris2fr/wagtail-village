postdeploy: python manage.py migrate && python manage.py update_index && python manage.py compilemessages
web: gunicorn wagtail_village.config.wsgi --log-file -
