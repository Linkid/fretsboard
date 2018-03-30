Installation
============

Settings (optional)
-------------------

Before running this application, you should configure some local settings:

- *SECRET_KEY*: you need to generate a new one
- *DEBUG*: default is True, which is not secured
- *ALLOWED_HOSTS*: the host you will use
- *DATABASES*: the database you will use (default is an SQLite one)
- *PIWIK_URL*: the URL of your Matomo instance
- *PIWIK_SITE_ID*: the id of your scoreboard instance


Run it locally
--------------

On a virtualenv::

    git clone git@github.com:Linkid/fretsboard.git
    cd fretsboard
    pip install -r requirements.txt
    ./manage.py migrate
    ./manage.py runserver


Run it on Heroku
----------------

Database used here: PostgreSQL
In your console::

    heroku login

    heroku apps:create your-scoreboard
    heroku addons:create heroku-postgresql --app your-scoreboard

    git remote set-url heroku git@heroku.com:your-scoreboard.git
    git push heroku master

    heroku ps:scale web=1
    heroku config:set SECRET_KEY=`openssl rand -base64 32`
    heroku run python manage.py migrate
    heroku open
