#!/bin/bash
EXT_ROOT=$1 
PY_ROOT=${EXT_ROOT}/py3
# Clean up PY_ROOT first 
rm -rf $PY_ROOT
mkdir -p ${EXT_ROOT}

# Create a python3 virtual environment at PY_ROOT 
python3 -m venv $PY_ROOT 

# Install dependencies 
$PY_ROOT/bin/pip install --upgrade pip
$PY_ROOT/bin/pip install Flask Flask-SQLAlchemy PyJWT 

# Create Asymmetric keys for JWT token signing
KEYS_DIR=${EXT_ROOT}/keys
mkdir -p $KEYS_DIR
openssl genpkey -algorithm RSA -out ${KEYS_DIR}/private_key.pem
openssl rsa -pubout -in ${KEYS_DIR}/private_key.pem -out ${KEYS_DIR}/public_key.pem
echo "Python virtual environment setup completed at ${PY_ROOT}"
echo "Asymmetric keys generated at ${KEYS_DIR}"