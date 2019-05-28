#!/usr/bin/env bash

virtualenv virtualenv -p python2
. virtualenv/bin/activate
pip install -r requirements.txt
deactivate

python3 -m venv virtualenv3
. virtualenv3/bin/activate
pip install -r requirements.txt
deactivate
