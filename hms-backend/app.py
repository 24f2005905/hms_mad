from flask import Flask 
import json
from flask_sqlalchemy import SQLAlchemy
import os 

from sqlalchemy import text 


app = Flask(__name__)
db = SQLAlchemy()  

@app.route("/", methods = ["GET"])
def hello_world():
    return "hello world!"


def init_db(db_uri, ddl_f_name):
    global db 
    global app 
    
    db_f_name = db_uri.removeprefix("sqlite:///")
    if os.path.exists(db_f_name): #Check if db already exists 
        return 0
    
    print(f"Creating the DB {db_f_name}")
    # Create the SQL Lite using Alchemy
    sql_script = open(ddl_f_name,'r').read() 
   
    # Run the sql script
    with app.app_context():
        raw_conn = db.engine.raw_connection()
        try:
            raw_conn.executescript(sql_script)
            raw_conn.commit()
        finally:
            raw_conn.close() 
    
    return 0 

@app.route("/hms/id/generate/token")

if __name__ == '__main__' :
    print(__name__)
    # Read the config from config.json
    config_dict = json.loads(open("config.json",'r').read())
    
    # Update the APP Config settings from config_dict
    app.config.update(config_dict["flask_config"])

    # Init the DB
    # Bind the db to the app
    db.init_app(app)

    init_db(app.config["SQLALCHEMY_DATABASE_URI"], config_dict["ddl_path"]);

    app.run(debug = True , port = config_dict['port'])