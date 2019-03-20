#!/usr/bin/env bash

virtualenv -p python3 env
source env/bin/activate
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
pip install -r requirements.txt
deactivate
