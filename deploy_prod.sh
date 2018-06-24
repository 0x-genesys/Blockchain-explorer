#pip install -r requirements.txt
python3 manage.py migrate --run-syncdb
python3 manage.py makemigrations
python3 manage.py migrate
python manage.py collectstatic
uwsgi deploy_config.ini &
uwsgi deploy_config_8081.ini &
