#!/bin/bash

cp libraries.txt requirements.txt
cat libraries-heroku.txt >> requirements.txt
cat libraries-vcs.txt >> requirements.txt
