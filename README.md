# 801Labs Hackerspace

django 2.1, python 3.6

## Setup

virtual environment

    virtualenv venv
    source venv/bin/activate

Install dependencies (django, braintree)

    pip install -r requirements.txt

Add [hackerspace/settings.py](hackerspace/settings.py) file

    cp hackerspace/settings.py.example hackerspace/settings.py

Add [braintree](https://www.braintreepayments.com/sandbox) settings, update APP_SECRET and database configuration in settings file.

Database setup

    python manage.py migrate

    python manage.py loaddata member_levels.yaml
    python manage.py createsuperuser

    python manage.py runserver

Site http://127.0.0.1:8000/

Admin http://127.0.0.1:8000/admin

Emails

Default config uses file backend and stores emails in [tmp/app-messages](tmp/app-messages)

## Production

    # primarily for django admin css
    python manage.py collectstatic

The static is assumed to be at APP_ROOT/public, make sure the webserver routes traffic to wherever your STATIC_ROOT is set to.
