# INTRODUCTION

## This is a work in progress. We are looking for contributors/collaborators.

## Goals

* manage territory boundaries
* manage points of interest
* manage activity related to points of interest
* print territory maps along with associated points of interest

## Technologies

* python
* django
* geodjango
* geos
* tastypie
* google maps
* backbone.js
* coffee.script
* jquery
* underscore

# INSTALLATION

## Windows

* easy_install -U pip
* pip install -U virtualenv
* mkdir /_envs
* cd /_envs
* virtualenv --no-site-packages flt
* /_envs/flt/Scripts/activate.bat
* pip install -r requirements.txt
* cd /_flt
* pip install django-evernote-oauth
* mv django-evernote-oauth evernote_oauth
* python manage.py syncdb
* python manage.py runserver

# ACKNOWLEDGEMENTS

This project has been put together with a ton of help from a lot of people.

# LICENSE: GPL
