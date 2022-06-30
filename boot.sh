#!/bin/bash

# Structure copied from Mega Tutorial: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

flask db upgrade

exec gunicorn -b :5000 --access-logfile - --error-logfile - app:app

