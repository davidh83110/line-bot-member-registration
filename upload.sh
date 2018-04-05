#!/bin/bash

git add .
git commit -am "upload+`date`"
git push heroku master

