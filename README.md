CSDT Community Site
========

[![Build Status](https://drone.io/github.com/GK-12/rpi_csdt_community/status.png)](https://drone.io/github.com/GK-12/rpi_csdt_community/latest)

This project is sponsered by Rensselaer Polytechnic Institute's GK-12 fellowship under Dr. Ron Eglash. The goal is the create a web platform for students to share projects, community, and in general create a community around the pCSDT's. More information about the pCSDT's can be found here: http://csdt.rpi.edu/

## How-to deploy for development

Before setup you need:
* Python
* Python Virtualenv
* Python setup tools
* Libpq-dev
* Git
* Subversion
* Mercurial
* NPM
* Clone, fork, or download this repo

Setup for Linux:
```shell
cd {{ Directory of this repo }}
. ./activate

# for the time being you will need to select option 1 and timezone.now()
python ./manage.py makemigrations
python ./manage.py migrate
git submodule init
git submodule update

#Enter credentials as desired
python manage.py createsuperuser

# Every time you start to develop, start the server
#  It should auto refresh when you change a file
python ./manage.py runserver
```

Setup for Windows

```shell
cd {{ Directory of this repo }}
python virtualenv.py python
python ./python/bin/activate
python pip install -r ./libraries.txt.lock
python pip install -r ./libraries-vcs.txt
python pip install -r ./libraries-heroku.txt
npm install -g less

# for the time being you will need to select option 1 and timezone.now()
python ./manage.py makemigrations
python ./manage.py migrate
git submodule init
git submodule update

#Enter credentials as desired
python manage.py createsuperuser

# Every time you start to develop, start the server
#  It should auto refresh when you change a file
python ./manage.py runserver
```

Then you should be able to see the project at http://127.0.0.1:8000/

## How-to contribute

* Fork repo or if already forked, pull this repo to get latest.
* Make relevant issue on this repo

```
cd {{ Directory of this repo }}
git checkout -b {{name of changes}}
# Make changes
git add {{changed files}}
git commit
# Write a description
git push origin {{name of changes}}
# Make pull request on githup and reference your issue
git checkout develop (switch back to main branch for future pulls)
```
