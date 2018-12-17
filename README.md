# 801Labs Hackerspace

django 2.1, python 3.6

## Setup

Install dependencies

    pip install django braintree

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