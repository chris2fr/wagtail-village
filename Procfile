postdeploy: python manage.py migrate && python manage.py update_index && python manage.py compilemessages
web: gunicorn sites_faciles.config.wsgi --log-file -
