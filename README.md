# HMS
Hospital Mangement System - IIT Online BS Degree - MAD I Project


# Create Package
- Create the package using:
    bash py-env/gen_package.sh

- Package will be created as hms-mad.zip

# Install & Run

- Copy over hms-mad.zip to runtime environmment.
    cp hms-mad.zip <HMS MAD runtime>

- Unzip the hms-mad.zip
    unzip hms-mad.zip

- Generate the checksum
    echo "import checksumdir; dirhash = checksumdir.dirhash('hms-mad'); print(f'Checksum = {dirhash}')" | python3

- Create the Python Environment
    cd hms-mad
    bash py-env/setup_env.sh $PWD/ext

- Create the database and synthetic data
    cd hms-mad
    bash py-env/gen_db.sh localhost 5432 postgres mysecretpassword hms_db $PWD/sql

- Start the backend application. Runs flask in debug mode
    cd runtime
    cp ../hms-backend/config.json 
    ../ext/py3/bin/python3 ../hms-backend/app.py
    
- Start the front application in a separate shell. Runs flask in debug mode
    cd runtime
    cp ../hms-frontend/fe_config.json .
    ../ext/py3/bin/python3 ../hms-frontend/app.py

- Access the application in http://localhost:9001
    
