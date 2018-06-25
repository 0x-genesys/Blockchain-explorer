# bitcoin-data-migrator

Block files hex to SQL linked data. Allows fast seek and queries on the blockchain

TO INSTALL POSTGRESS ALONG WITH DJANGO:

1. sudo apt-get update


2. sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib


### Go into the subdirectory python-bitcoin-blockchain-parser through the command line and run the following command :

1. pip3 setup.py install


###CREATING DATABASE IN POSTGRES:

Run Command :

1. sudo -su postgres

2. psql

3. create database DATABASE_NAME;

4. create user PROJECT_USER with password 'PASSWORD';

5. GRANT ALL PRIVILEGES ON DATABASE DATABASE_NAME TO PROJECT_USER;

> DO NOT FORGET THE SEMICOLON

TO EXIT THE POSTGRES SHELL

6. \q

7. exit


After installing the postgres, make changes in the settings.py file of your Django project

folder:


## Look for DATABASES = {}


  DATABASES = {

      'default': {

          'ENGINE': 'django.db.backends.postgresql',

          'NAME': 'myprojectdb',

          'USER': 'PROJECT_USER',

          'PASSWORD': 'PASSWORD',

          'HOST':'localhost',

          'PORT':'',

          #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),

      }
  }

## Change these lines in populate_sql.py in the populate folder

1. Change the path of the BLOCK_DATA_DIR + 'path where your bitcoin_data is stored'


## Make these changes and then follow these steps in order:

1. Change your directory to the django project folder from command line.

2. python3 manage.py migrate --run-syncdb

3. python3 manage.py createsuperuser

4. set your username and password for Django-Admin

5. python3 manage.py makemigrations

6. python3 manage.py migrate

7. python3 manage.py runserver


### Now open browser and type in the url field :  127.0.0.0:8000/run

### You can also check your admin panel by :  127.0.0.0:8000/admin


###DEPLOYMENT:


Nginx is listening on 80

2 instance of uwsgi running on 8080 and 8081

one ebl for 500gb

psql database

bitcoin node

4gb ram dual core 18 gb disk server

OS ubuntu

ref:

https://www.digitalocean.com/community/tutorials/how-to-deploy-python-wsgi-applications-using-uwsgi-web-server-with-nginx

http://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html

note: be careful with nginx static files and running migrations

###commands:

alias karan-available_devices="df"

alias karan-give_access="sudo chown `whoami`"

alias karan-bitcoin-cli="bitcoin-cli -datadir=/data/bitcoin/ -rpcuser=karan -rpcpassword=blockwala@123"

alias karan-psql-cli="sudo -u postgres psql postgres"

alias karan-check-swap="grep 'Swap' /proc/meminfo"

alias karan-check-mem="watch -n 5 free -m"

alias karan-virtualenv-start="source bitcoinenv/bin/activate"

alias karan-postgres-start="sudo -u postgres psql postgres"

alias karan-start-bitcoind="bitcoind -datadir='/data/bitcoin/' -daemon -rpcuser=karan -rpcpassword=blockwala@123"

alias karan-clock-speed-cpu="lscpu | grep MHz"

alias karan-postgres="/etc/init.d/postgresql"

alias karan-nginx-start="sudo service nginx start"

alias karan-nginx-stop="sudo service nginx stop"

alias karan-nginx-status="sudo service nginx status"

alias karan-bitcoin-app-runserver-uwsgi-http="uwsgi --socket 127.0.0.1:8000 --protocol=http -w app.wsgi"

alias karan-bitcoin-app-server-logs=" tail -f /var/log/uwsgi/app_uwsgi.log"

alias karan-bitcoin-app-server-stop="uwsgi --stop /tmp/app.pid"

alias karan-bitcoin-app-server-restart="uwsgi --reload /tmp/app.pid"

alias karan-nginx-start="sudo service nginx start"

alias karan-nginx-stop="sudo service nginx stop"

alias karan-nginx-view-config="sudo vi /etc/nginx/nginx.conf"


