CSDT Community Site
========

[![Build Status](https://travis-ci.org/CSnap/rpi_csdt_community.svg?branch=master)](https://travis-ci.org/CSnap/rpi_csdt_community)

This project is sponsered by Rensselaer Polytechnic Institute's GK-12 fellowship under Dr. Ron Eglash. The goal is the create a web platform for students to share projects, community, and in general create a community around the pCSDT's. More information about the pCSDT's can be found here: http://csdt.rpi.edu/

## How-to deploy for development

Before setup you need:
* Python 2.X
* Python Virtualenv
* Python setup tools
* Libpq-dev
* Git
* Subversion
* Mercurial
* NPM & Node
* This repo (clone, fork, or download)

Setup for Linux:
```shell
cd {{ Directory of this repo }}
. ./activate
sudo npm install -g less
sudo npm install -g yuglify

# For the time being you will need to select option 1 and timezone.now()
python ./manage.py migrate
git submodule init
git submodule update

# Enter credentials as desired
python manage.py createsuperuser

# Every time you start to develop, start the server
#  It should auto refresh when you change a file
python ./manage.py runserver
```

Setup for Windows

```shell
cd {{ Directory of this repo }}
virtualenv python
python\Scripts\activate.bat
npm install -g less
npm install -g yuglify
pip install -r ./libraries.txt.lock
pip install -r ./libraries-vcs.txt
pip install -r ./libraries-heroku.txt

# For the time being you will need to select option 1 and timezone.now()
python ./manage.py migrate
git submodule init
git submodule update

# Enter credentials as desired
python manage.py createsuperuser

# Every time you start to develop, start the server
#  It should auto refresh when you change a file
python ./manage.py runserver
```

Then you should be able to see the project at http://127.0.0.1:8000/

## How-to contribute

* Fork repo or if already forked, pull this repo to get latest.
* Make relevant issue on this repo

```shell
cd {{ Directory of this repo }}
git checkout -b {{name of changes to be made}}
# Make changes
git add -A
git commit
# Write a description
git push origin {{name of changes}}
# Make pull request on githup and reference your issue
git checkout master
```
