#!/bin/bash

# Setup the NodeJS PPA
curl -sL https://deb.nodesource.com/setup_6.x -o nodesource_setup.sh
sudo bash nodesource_setup.sh
rm nodesource_setup.sh

sudo apt-get update
sudo apt-get upgrade

# Install python
sudo apt-get install -y python-pip python-dev

# Install the database
sudo apt-get install -y postgresql postgresql-contrib postgis
# Set password
sudo -u postgres psql -U postgres -d postgres -c "alter user postgres with password 'postgres';"
# Create the database
sudo -u postgres createdb rpi_csdt_community

# Add extensions to database
CREATE EXTENSION postgis;
CREATE EXTENSION postgis_topology;

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
