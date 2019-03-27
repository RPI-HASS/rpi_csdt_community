#!/bin/bash

# Setup the NodeJS PPA
curl -sL https://deb.nodesource.com/setup_6.x -o nodesource_setup.sh
sudo bash nodesource_setup.sh
rm nodesource_setup.sh

sudo apt-get install binutils libproj-dev gdal-bin

sudo apt-get update
sudo apt-get upgrade

# Install python
sudo apt-get install python-pip python-dev
# Install postgis
sudo apt-get install -y libpq-dev libcurl4-openssl-dev postgresql postgis

# Install the database
sudo apt-get install -y postgresql postgresql-contrib 
# Set password
sudo -u postgres psql -U postgres -d postgres -c "alter user postgres with password 'postgres';"
# Create the database
sudo -u postgres createdb rpi_csdt_community
# Add Extensions
sudo -u postgres psql rpi_csdt_community -c "CREATE EXTENSION adminpack; CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;"

# Install node
sudo apt-get install -y nodejs build-essential

sudo npm install -g less


sudo apt-get install -y python-setuptools

sudo easy_install pip


# Install libraries for the community site
sudo apt-get install -y  libpq-dev libcurl4-openssl-dev
pip install --upgrade -r /vagrant/requirements.txt

# Install the git submodules
cd /vagrant/
git submodule init
git submodule update
git submodule add


# Run migrations to init db
python manage.py migrate
