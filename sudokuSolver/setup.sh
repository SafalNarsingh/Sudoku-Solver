#!/bin/hash

# Install the required dependencies
pip install setuptools
pip install -r requirements.txt

#Run django commands
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic 