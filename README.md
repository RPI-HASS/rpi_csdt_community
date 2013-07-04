= CSDT Community Site =

This project is sponsered by Rensselaer Polytechnic Institute's GK-12 fellowship under Dr. Ron Eglash. The goal is the create a web platform for students to share projects, community, and in general create a community around the pCSDT's. More information about the pCSDT's can be found here: http://csdt.rpi.edu/

== How-to deploy for development ==

To deploy this project, you will need the following packages installed:
* Python Virtualenv
* Python setup tools
* Everything you need to compile python-pil
** This can be done (on debian-based systems) by running apt-get build-dep python-pil
** libz, libjpeg, libfreetype2
* git, subversion, and mercurial (I know... but several of the packages I need haven't yet been updated in pypy)

Now, the howto
```shell
cd {{ Directory of this repo }}
cd src
. ./activate
cd src
python ./manage.py syncdb
python ./manage.py runserver
```

Then you should be able to see the project at http://127.0.0.1:8000/

== How-to deploy for production ==

To much work. I would suggest using mod_wsgi. There is a sample configuration file in the doc/ folder.

== How-to contribute ==

Fork this repo, make your changes. Be sure to justify everything! Avoid anything too tricky, try to stick to Django's principles (reuse other libraries, DRY). When you're ready to share what you've done, make a pull request)
