import json
import os 
import jwt
import uuid
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text 
from datetime import datetime, timedelta, date
from functools import wraps



app = Flask(__name__)
db = SQLAlchemy()  
jwt_private_str = None
jwt_public_str = None
Valid_User_Types = [
    "DOCTOR", "PATIENT", "ADMIN"
]
Valid_User_Column = [
    "User_ID", "First_Name", "Last_Name", 
    "User_Type", "Phone_Number","User_Profile",
    "Password"
]
@app.route("/", methods = ["GET"])
def hello_world():
    return "hello world!"


def init_db(db_uri, ddl_f_name):
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

def auth_wrapper(f):
    """ Auth Wrapper Decorator"""
    @wraps(f)
    def token_wrapper(*args, **kwargs):
        # Check Auth header
        apiKey = request.headers.get("Authorization")
        auth_args = {}
        auth_args['auth_token'] = None
        try:
            auth_args['auth_token'] = jwt.decode(apiKey, jwt_public_str, algorithms = ["RS256"])
        except Exception as e:
            auth_args["auth_err"] = f"Invalid apiKey: {str(e)}"
        kwargs['auth_args'] = auth_args
        return f(*args, **kwargs)
    return token_wrapper

@app.route("/hms/id/generate/token", methods=["POST"])
def id_token_generate():
    req_json = request.get_json()

    if "User_ID" not in req_json or "Password" not in req_json:
        return {"status":"error", "message":"Invalid request"}, 400
    
    User_ID = req_json["User_ID"]
    Password = req_json["Password"]

    query = text("SELECT User_Type, Password FROM Users WHERE User_ID = :user_id")
    password = None
    with app.app_context():
        result = db.session.execute(query,{"user_id": User_ID})
        details = result.fetchone()
        if details:
            Role = details[0]
            password = details[1] #Fetch password corresponding to User_ID
    
    #Password verification
    if not password:
        return {"status":"error", "message":"Login Failed"}, 401
    else:
        if Password != password:
            return {"status":"error", "message":"Login Failed"}, 401
    
    start_time = datetime.utcnow().timestamp()
    exp = (datetime.utcnow() + timedelta(hours = 8)).timestamp()
   
    auth_token = {
        'id': str(uuid.uuid4()),
        'user': User_ID, 
        'role': Role, 
        'iat': 
        int(start_time), 
        'exp': int(exp) 
    }
    auth_token_str = jwt.encode(auth_token,jwt_private_str, algorithm = "RS256")
    return {
        "status":"succeess", 
        "token": auth_token_str
    }, 200

@app.route("/hms/user/create", methods=["POST"])
@auth_wrapper
def User_Create(auth_args):
    ret = {"status": "success"}
    # Check Auth
    if not auth_args['auth_token']:
        ret["status"] = "error"
        ret["message"] = auth_args["auth_err"]
        return ret, 401
    
    # Get the request body
    req_json = request.get_json()

    # Check for Mandatory Fields
    if "First_Name" not in req_json or \
        "User_Type" not in req_json or \
        "Phone_Number" not in req_json or \
        "Password" not in req_json :
        ret["status"] = "error"
        ret["message"] = "Invalid request: Missing Mandatory Fields"
        return ret, 400
    
    # Check for valid User_Type
    if req_json["User_Type"] not in Valid_User_Types:
        ret["status"] = "error"
        ret["message"] = f"Invalid User Type: {req_json['User_Type']}"
        return ret, 400
    
    User_Type = req_json["User_Type"]
    
    # Generate an ID: [P/A/D]-YYYY-MM-DD-[SNO]
    # Query for all User IDs for partial match
    query_1 = text("SELECT User_ID FROM Users WHERE User_ID LIKE :partial_match ORDER BY id DESC")
    partial_match = f'{User_Type[0]}-{date.today().strftime("%Y-%m-%d")}-'
    serial_no = 1
    with app.app_context():
        result = db.session.execute(query_1,{"partial_match": partial_match+'%' })
        matches = result.fetchone()
    if matches: 
        serial_no = int(matches[0].split('-')[-1]) + 1
    User_ID = f"{partial_match}{serial_no:03d}"

    # Now insert the user
    query_2 = text ('INSERT INTO Users '\
        '(User_ID, First_Name, Last_Name, ' \
        'User_Type, Phone_Number, User_Profile, Password) ' \
        'VALUES (:User_ID, ' \
        ':First_Name, :Last_Name, :User_Type,' \
        ':Phone_Number, :User_Profile, :Password)')
    query_2_dict = {
        "User_ID": User_ID,
        "First_Name": req_json["First_Name"],
        "Last_Name": req_json.get("Last_Name",""),
        "User_Type": User_Type,
        "Phone_Number": req_json["Phone_Number"],
        "User_Profile": req_json.get("User_Profile",""),
        "Password": req_json["Password"]
    }
    with app.app_context():
         result = db.session.execute(query_2,query_2_dict)
         db.session.commit()
        
    ret["User_ID"] = User_ID
    return ret, 200

@app.route("/hms/user/lookup", methods=["GET"])
@auth_wrapper
def User_Lookup(auth_args):
    ret = {"status": "success"}
    # Check Auth
    if not auth_args['auth_token']:
        ret["status"] = "error"
        ret["message"] = auth_args["auth_err"]
        return ret, 401
    auth_token = auth_args['auth_token']
    
    #Get parameters
    param_json = request.args.to_dict()
    match_clauses = []
    for key in ['User_ID','Phone_Number','First_Name','Last_Name']:
        if key in param_json:
            match_clauses.append(f"LOWER({key}) LIKE LOWER('%{param_json[key]}%')")
    query = "SELECT * FROM Users "
    if len(match_clauses):
        query += " WHERE "
        query += " AND ".join(match_clauses)
    print(f"QUERY: {query}")
    with app.app_context():
        result = db.session.execute(text(query))
        rows = result.fetchall() 
    
    user_details = []
    for row_ent in rows:
        row_dict = (dict(row_ent._mapping))
        row_dict.pop('Password')
        if auth_token['role'] == 'ADMIN' or \
            auth_token['role'] == 'DOCTOR' and row_dict['User_ID'][0] == 'P' or \
            auth_token['user'] == row_dict['User_ID']:
            user_details.append(row_dict)

    ret['user_details'] = user_details 
    return ret, 200

@app.route("/hms/user/update", methods=["POST"])
@auth_wrapper
def User_Update(auth_args):
    ret = {"status": "success"}
    # Check Auth
    if not auth_args['auth_token']:
        ret["status"] = "error"
        ret["message"] = auth_args["auth_err"]
        return ret, 401
    auth_token = auth_args['auth_token']

    # Get the request body
    req_json = request.get_json()

    #Checking for User_ID 
    if 'User_ID' not in req_json:
        ret["status"] = "error" 
        ret["message"] = "User_ID not found"
        return ret, 400
    
    # Enforce Role Here
    if auth_token['role'] != 'ADMIN' and \
            auth_token['User_ID'] != req_json['User_ID']:
            ret["status"] = "error" 
            ret["message"] = "Update unauthorized"
            return ret, 403
    
    # Check for User ID
    query_check = f"SELECT User_ID from Users WHERE User_ID = '{req_json['User_ID']}'"
    with app.app_context():
        result = db.session.execute(text(query_check))

    if result.rowcount != 1:
        ret["status"] = "error" 
        ret["message"] = "User Not Found"
        return ret, 400

    query = "UPDATE Users SET "
    updates = []

    for column_name in req_json:
        if column_name not in Valid_User_Column:
            ret["status"] = "error" 
            ret["message"] = "Invalid Attribute"
            return ret, 400
        
        if column_name == 'User_ID':
            continue 
        updates.append(f"{column_name} = '{req_json[column_name]}'")
    
    if not updates:
        ret["status"] = "error" 
        ret["message"] = "No field to update"
        return ret, 400

    query += ",".join(updates)
    query += f" WHERE User_ID = '{req_json['User_ID']}';"

    with app.app_context():
        result = db.session.execute(text(query))
        db.session.commit()
    
    if result.rowcount != 1:
        ret["status"] = "error" 
        ret["message"] = "Failed to update"
        return ret, 400
    
    ret["User_ID"] = req_json["User_ID"]
    ret["query"] = query
   
    return ret, 200

if __name__ == '__main__' :
    print(__name__)
    # Read the config from config.json
    config_dict = json.loads(open("config.json",'r').read())
    
    # Load JWT Private and Public Keys
    jwt_private_str = open(config_dict["jwt_private"]).read()
    jwt_public_str = open(config_dict["jwt_public"]).read()

    # Update the APP Config settings from config_dict
    app.config.update(config_dict["flask_config"])

    # Init the DB
    # Bind the db to the app
    db.init_app(app)

    init_db(app.config["SQLALCHEMY_DATABASE_URI"], config_dict["ddl_path"]);

    app.run(debug = True , port = config_dict['port'])
    