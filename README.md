# bitcoin-data-migrator

Block files hex to SQL linked data. Allows fast seek and queries on the blockchain

TO INSTALL POSTGRESS ALONG WITH DJANGO:

1. sudo apt-get update


2. sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib



CREATING DATABASE IN POSTGRES:

Run Command :

1. sudo -su postgres

2. psql

3. create database DATABASE_NAME;

4. create user PROJECT_USER with password 'PASSWORD';

5. GRANT ALL PRIVILEGES ON DATABASE DATABASE_NAME TO PROJECT_USER;

DO NOT FORGET THE SEMICOLON

6. \q

7. exit


After installing the postgres, make changes in the settings.py file of your Django project

folder:


# Look for DATABASES = {}


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

  
# Make these changes and then follow these steps in order:

1. Change your directory to the django project folder from command line.

2. python3 manage.py migrate --run-syncdb

3. python3 manage.py createsuperuser

4. set your username and password for Django-Admin

5. python3 manage.py makemigrations

6. python3 manage.py migrate

7. python3 manage.py runserver


 Now open browser and type in the url field : # '127.0.0.0:8000/run'

 You can also check your admin panel by : # '127.0.0.0:8000/admin'
