#!/bin/bash


# Setup the NodeJS PPA
curl -sL https://deb.nodesource.com/setup_6.x -o nodesource_setup.sh
sudo bash nodesource_setup.sh
rm nodesource_setup.sh

sudo apt-get install binutils libproj-dev gdal-bin


# Install node
sudo apt-get install -y nodejs build-essential
sudo npm install -g less


# Install libraries for the community site
sudo apt-get install -y  libpq-dev libcurl4-openssl-dev
sudo apt-get install -y build-essential libssl-dev libffi-dev \
     libxml2-dev libxslt1-dev zlib1g-dev gdal-bin

sudo apt install -y git

# Install the git submodules
cd /csdt_site/
git submodule init
git submodule update

which python
