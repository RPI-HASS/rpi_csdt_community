import os, sys

try:
    from setuptools import setup
except:
    from distutils.core import setup

from setuptools.command.test import test

def run_tests(*args):
    import subprocess
    errors = subprocess.Popen(["coverage", "run", "src/rpi_csdt_community/tests/runtests.py"]).wait()
    if errors:
        sys.exit(1)
    else:
        sys.exit(0)

test.run_tests = run_tests

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def read_requirements(fname):
    f = open(os.path.join(os.path.dirname(__file__), fname))
    return filter(lambda f: f != '', map(lambda f: f.strip(), f.readlines()))

setup(
    zip_safe = False,
    name = "rpi_csdt_community",
    version = "1.0.0",
    author = "Charles Hathaway",
    author_email = "hathac@rpi.edu",
    description = ("The community site for RPI's CSDT initiative"),
    license = "BSD",
    keywords = "rpi csdt pcsdt community",
    url = "http://community.csdt.rpi.edu/",
    package_dir = {'': 'src/rpi_csdt_community'},
    packages=['rpi_csdt_community', 'project_share'],
    package_data={'rpi_csdt_community': ['../templates/*.html',
                                         '../templates/*/*.html',
                                         '../static/bootstrap/css/bootstrap.css',
                                         '../static/current/*/*.jar',
                                         '../static/current/*/*/*.jar',
                                         '../static/current/*/*.jnlp'],
                  'project_share': ['templates/project_share/*.html']},
    long_description=read('README.md'),
    install_requires = read_requirements('src/libraries.txt'),
    test_suite = "dummy",
)
