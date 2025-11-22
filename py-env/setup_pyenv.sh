#!/bin/bash 
PY_ROOT=$1
# Clean up PY_ROOT first 
rm -rf $PY_ROOT

# Create a python3 virtual environment at PY_ROOT 
python3 -m venv $PY_ROOT 

# Install dependencies 
$PY_ROOT/bin/pip install --upgrade pip
$PY_ROOT/bin/pip install Flask Flask-SQLAlchemy PyJWT 

