#!/bin/bash

# Setup the NodeJS PPA
curl -sL https://deb.nodesource.com/setup_6.x -o nodesource_setup.sh
sudo bash nodesource_setup.sh
rm nodesource_setup.sh

sudo apt-get update
sudo apt-get upgrade

# Install python
sudo apt-get install -y python-pip python-dev
# Install postgis
sudo apt-get install -y libpq-dev libcurl4-openssl-dev postgresql postgis

# Install the database
sudo apt-get install -y postgresql postgresql-contrib 
# Set password
sudo -u postgres psql -U postgres -d postgres -c "alter user postgres with password 'postgres';"
# Create the database
sudo -u postgres createdb rpi_csdt_community
# Add Extensions
<<<<<<< HEAD
#echo 'rpi_csdt_community; CREATE EXTENSION adminpack; CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;' | psql -U postgres
#/////////////////
sudo su - postgres
psql rpi_csdt_community
CREATE EXTENSION adminpack;
CREATE EXTENSION postgis;
CREATE EXTENSION postgis_topology;
\q
cd /vagrant/
#/////////////////

=======
echo 'rpi_csdt_community; CREATE EXTENSION adminpack; CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;' | psql -U postgres

#echo "GOOGLE_API_KEY = "rgsehsfgsdfbsfdgxvfx532dfe52"" > /usr/local/lib/python2.7/dist-packages/gis_csdt/settings.py
#echo "CENSUS_API_KEY = "gfsgerultiahefb4u9834tkbrfsb"" > /usr/local/lib/python2.7/dist-packages/gis_csdt/settings.py
>>>>>>> d983c3340b8dc0542511fcd7d6175d5f3e72b035
# Install node
sudo apt-get install -y nodejs build-essential

sudo npm install -g less

# Install libraries for the community site
sudo apt-get install -y  libpq-dev libcurl4-openssl-dev
pip install --upgrade pip
pip install --upgrade -r /vagrant/requirements.txt

# Install the git submodules
cd /vagrant/
git submodule init
git submodule update

#add dataset
python manage.py makemigrations gis_csdt

# Run migrations to init db
python manage.py migrate
