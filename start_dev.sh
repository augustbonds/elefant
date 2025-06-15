#!/bin/bash
source venv/bin/activate
export FLASK_APP=elefant.py
export FLASK_ENV=development
flask run --host=127.0.0.1 --port=5000