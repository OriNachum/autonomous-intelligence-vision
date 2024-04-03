#!/bin/bash

cd /home/ori/git/tau-jetson-ext
source .venv/bin/activate

python3 tau_ext.py
#uvicorn app:app --host 0.0.0.0 --port 8000 --reload
