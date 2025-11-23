import json
import os 
import jwt
import uuid
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text,exc
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
Valid_Days_Of_Week = [
    "mon", "tue", "wed", "thu", "fri", "sat", "sun"
]

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

    query = text("SELECT User_Type, Password, User_Status FROM Users WHERE User_ID = :user_id and User_Status = 'ACTIVE'")
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
  
    with app.app_context():
        result = db.session.execute(text(query))
        rows = result.fetchall() 
    
    user_details = []
    for row_ent in rows:
        row_dict = (dict(row_ent._mapping))
        row_dict.pop('Password')
        row_dict.pop('id')
        if auth_token['role'] == 'ADMIN' or \
            auth_token['role'] == 'DOCTOR' and row_dict['User_ID'][0] == 'P' and \
                 row_dict['User_Status'] == 'ACTIVE' or \
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
            auth_token['user'] != req_json['User_ID']:
            ret["status"] = "error" 
            ret["message"] = "Update unauthorized"
            return ret, 403
    
    # Check for User ID
    query_check = f"SELECT User_ID from Users WHERE User_ID = '{req_json['User_ID']}';"
    with app.app_context():
        result = db.session.execute(text(query_check))
        rows = result.fetchall()
    
    if len(rows) != 1:
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
        row = result.fetchall()
        db.session.commit()
    
    if row.rowcount != 1:
        ret["status"] = "error" 
        ret["message"] = "Failed to update"
        return ret, 400
    
    ret["User_ID"] = req_json["User_ID"]
    ret["query"] = query
   
    return ret, 200

@app.route("/hms/user/delete", methods=["DELETE"])
@auth_wrapper
def User_Delete(auth_args):
    ret = {"status": "success"}
    # Check Auth
    if not auth_args['auth_token']:
        ret["status"] = "error"
        ret["message"] = auth_args["auth_err"]
        return ret, 401
    auth_token = auth_args['auth_token']

    #Get parameters
    param_json = request.args.to_dict()
    if 'User_ID' not in param_json:
        ret["status"] = "error"
        ret["message"] = "User ID Not Provided"
        return ret, 400
    
    User_ID = param_json["User_ID"]
   
   #Enforce Role
    if auth_token['role'] != 'ADMIN':
        ret["status"] = "error" 
        ret["message"] = "Delete Unauthorized"
        return ret, 403 
    
    if User_ID == 'ADMIN': 
        ret["status"] = "error" 
        ret["message"] = "Cannot Delete Super Admin"
        return ret, 400 
    
    #Verifying User_ID existence
    query_1 = f"SELECT User_ID FROM Users WHERE User_ID = '{User_ID}';"
    with app.app_context():
        result = db.session.execute(text(query_1))
        rows = result.fetchall() 
   
    if len(rows) != 1:
        ret["status"] = "error" 
        ret["message"] = "User Not Found"
        return ret, 400
    
    #Query for deletion
    query =  f"UPDATE Users SET User_Status = 'INACTIVE' WHERE User_ID = '{User_ID}';"
    with app.app_context():
        result = db.session.execute(text(query))
        db.session.commit()
    ret["User_ID"] = User_ID 
    return ret, 200
    
@app.route("/hms/departments/create", methods=["POST"])
@auth_wrapper
def Dept_Create(auth_args):
    ret = {"status": "success"}
    # Check Auth
    if not auth_args['auth_token']:
        ret["status"] = "error"
        ret["message"] = auth_args["auth_err"]
        return ret, 401
    auth_token = auth_args['auth_token']

    #Enforce Role
    if auth_token['role'] != 'ADMIN':
        ret["status"] = "error" 
        ret["message"] = "Unauthorized Access"
        return ret, 403 
    
    # Get the request body
    req_json = request.get_json()

    #Check for Mandatory Fields
    if "Speciality" not in req_json:
        ret["status"] = "error"
        ret["message"] = "Invalid request: Missing Mandatory Fields"
        return ret, 400 
    
  
    #Generate Dept_ID : Dept-001 
    partial_match = 'Dept-'
    serial_no = 1 
    query = text("SELECT Dept_ID FROM Departments WHERE Dept_ID LIKE :partial_match ORDER BY id DESC")
    with app.app_context():
        result = db.session.execute(query,{"partial_match": partial_match+'%' })
        matches = result.fetchone()
    if matches: 
        serial_no = int(matches[0].split('-')[-1]) + 1
    Dept_ID = f"{partial_match}{serial_no:03d}"

    # Updating Database 
    query_1 = text("INSERT INTO Departments  " \
    "(Dept_ID, Speciality, Details) VALUES "\
    "(:Dept_ID, :Speciality, :Details)")

    query_1_dict = {"Dept_ID": Dept_ID, "Speciality": req_json["Speciality"], "Details": req_json.get("Details","")}
    
    with app.app_context():
        try:
            result = db.session.execute(query_1,query_1_dict)
            db.session.commit()
        except exc.IntegrityError:
            ret["status"] = "error"
            ret["message"] = f"Department {req_json['Speciality']} already exists."
            return ret, 400
        
    ret["Dept_ID"] = Dept_ID
    return ret, 200

@app.route("/hms/departments/lookup", methods=["GET"])
@auth_wrapper
def Dept_Lookup(auth_args):
    ret = {"status": "success"}
    # Check Auth
    if not auth_args['auth_token']:
        ret["status"] = "error"
        ret["message"] = auth_args["auth_err"]
        return ret, 401
    auth_token = auth_args['auth_token']

    #Enfore Roles
    if auth_token['role'] != 'ADMIN':
        ret["status"] = "error" 
        ret["message"] = "Lookup Unauthorized"
        return ret, 403 
    
    #Get parameters
    param_json = request.args.to_dict()  

    #Query Database
    match_clauses = []
    for key in ["Dept_ID","Speciality"]:
        if key in param_json:
            match_clauses.append(f"LOWER({key}) LIKE LOWER('%{param_json[key]}%')")
    
    query = "SELECT * FROM Departments"
    if len(match_clauses):
        query += " WHERE "
        query += " AND ".join(match_clauses)
        query += ";"
    
    with app.app_context():
        result = db.session.execute(text(query))
        rows = result.fetchall() 
    
    department_details = []
    for entry in rows:
        row_dict =(dict(entry._mapping))
        row_dict.pop('id')
        department_details.append(row_dict)
    
    ret["department_details"] = department_details

    return ret, 200 

@app.route("/hms/departments/delete", methods=["DELETE"])
@auth_wrapper
def Dept_Delete(auth_args):
    ret = {"status": "success"}
    # Check Auth
    if not auth_args['auth_token']:
        ret["status"] = "error"
        ret["message"] = auth_args["auth_err"]
        return ret, 401
    auth_token = auth_args['auth_token']

    #Get parameters
    param_json = request.args.to_dict()
    if 'Dept_ID' not in param_json:
        ret["status"] = "error"
        ret["message"] = "User ID Not Provided"
        return ret, 400
    
    Dept_ID = param_json["Dept_ID"]

    #Enforcing Roles
    if auth_token['role'] != 'ADMIN':
        ret["status"] = "error" 
        ret["message"] = "Delete Unauthorized"
        return ret, 403 

    #Ensuring Department Exists
    query_1 = f"SELECT Dept_ID FROM Departments WHERE Dept_ID = '{Dept_ID}';"
    with app.app_context():
        result = db.session.execute(text(query_1))
        rows = result.fetchall()
    
    if len(rows) != 1:
        ret["status"] = "error" 
        ret["message"] = "Department Not Found"
        return ret, 400

    query_2 = f"DELETE FROM Departments WHERE Dept_ID = '{Dept_ID}';"
    with app.app_context():
        result = db.session.execute(text(query_2))
        db.session.commit()
    ret["Dept_ID"] = Dept_ID 
    return ret, 200

@app.route("/hms/slots/create", methods=["POST"])
@auth_wrapper
def Slots_Create(auth_args):
    ret = {"status": "success"}
    # Check Auth
    if not auth_args['auth_token']:
        ret["status"] = "error"
        ret["message"] = auth_args["auth_err"]
        return ret, 401
    auth_token = auth_args['auth_token']
    # Get the request body
    req_json = request.get_json()  

    #Checking for mandatory fields
    if "Doctor_ID" not in req_json or \
        "Days_Available" not in req_json or \
        "Start_Date" not in req_json or \
        "End_Date" not in req_json:
        ret["status"] = "error"
        ret["message"] = "Invalid request: Missing Mandatory Fields"
        return ret, 400 
    
    #Enforcing Role 
    if auth_token['role'] == 'PATIENT' or \
        (auth_token['role'] == 'DOCTOR' and auth_token['user'] != req_json["Doctor_ID"]):
        ret["status"] = "error"
        ret["message"] = "Unauthorized"
        return ret, 400
    
    #Check Valid User 
    query_1 = "SELECT User_ID FROM Users " \
        f"WHERE User_ID = '{req_json['Doctor_ID']}' AND " \
        "User_Status = 'ACTIVE'"
    with app.app_context():
        result = db.session.execute(text(query_1))
        rows = result.fetchone()
    
    if len(rows) != 1 :
        ret["status"] = "error"
        ret["message"] = "Invalid User"
        return ret, 400
    
    #Check valid date format
    try:
        Start_Date = datetime.strptime(req_json["Start_Date"],'%Y-%m-%d').date()
        End_Date = datetime.strptime(req_json["End_Date"],'%Y-%m-%d').date()
        if End_Date < Start_Date:
             ret["status"] = "error"
             ret["message"] = "Invalid Date Range"
             return ret, 400
    except:
        ret["status"] = "error"
        ret["message"] = "Invalid Date Format"
        return ret, 400
    
    #Define valid day of week 
    for day in req_json["Days_Available"]:
        if day.lower() not in Valid_Days_Of_Week:
            ret["status"] = "error"
            ret["message"] = "Invalid Day Of Week"
            return ret, 400

   #Check existence of Doctor_ID
    query_2 = text("SELECT Doctor_ID,Start_Date,End_Date FROM Slots WHERE Doctor_ID = :Doctor_ID")
    with app.app_context():
        result = db.session.execute(query_2,{"Doctor_ID": req_json["Doctor_ID"]})
        rows = result.fetchone()
   
   #If Doctor_ID exists, update row instead
    if rows:
        print(rows)
        Old_Start_Date = rows[1]
        Old_End_Date = rows[2]
        
        open_app_query = "SELECT Appointment_ID FROM Appointments  " \
            "WHERE Appointment_Status = 'SCHEDULED' AND " \
            f"Doctor_ID = '{req_json['Doctor_ID']}' AND " \
            f"(Appointment_Date BETWEEN '{Old_Start_Date}' AND '{Old_End_Date}');"
        
        print(open_app_query)
        
        with app.app_context():
            open_appointments = db.session.execute(text(open_app_query))
            rows = open_appointments.fetchall()

        if len(rows):
            ret["status"] = "error" 
            ret["message"] = "Clear Existing Appointments before updating slots"
            return ret, 400 

        # There are no existing appointments. Delete the old Slot
        del_old_slot_q = text(f"DELETE from Slots WHERE Doctor_ID = '{req_json['Doctor_ID']}'")
        with app.app_context():
            del_old_slots = db.session.execute(del_old_slot_q)
            #row = del_old_slots.fetchall()
            db.session.commit()
        
        if del_old_slots.rowcount != 1:
            ret["status"] = "error" 
            ret["message"] = "Error Deleting Old Slot"
            return ret, 500 
            
       

    #Creating new slot      
    query_3 = text("INSERT INTO Slots  " \
    "(Doctor_ID, Days_Available, Start_Date, End_Date) VALUES "\
    "(:Doctor_ID, :Days_Available, :Start_Date, :End_Date)")

    query_3_dict = {
        "Doctor_ID": req_json["Doctor_ID"], "Days_Available": json.dumps(req_json["Days_Available"]), 
        "Start_Date": req_json["Start_Date"], "End_Date": req_json["End_Date"]
        }
    
    with app.app_context():
        result = db.session.execute(query_3,query_3_dict)
        db.session.commit()

    ret["Doctor_ID"] = req_json['Doctor_ID']
    return ret, 200

@app.route("/hms/slots/lookup", methods=["GET"])
@auth_wrapper
def Slots_Lookup(auth_args):
    ret = {"status": "success"}
    # Check Auth
    if not auth_args['auth_token']:
        ret["status"] = "error"
        ret["message"] = auth_args["auth_err"]
        return ret, 401
   
    #Get parameters
    param_json = request.args.to_dict()
    Doctor_ID = param_json["Doctor_ID"]

    #Check Current Date
    Current_Date = datetime.now().strftime("%Y-%m-%d") 

    #Check Doctor_Status 
    doctor_status_q = text("SELECT User_Status FROM Users " \
                          f"WHERE User_ID = '{Doctor_ID}' AND User_Status = 'ACTIVE'")
    with app.app_context():
        result = db.session.execute(doctor_status_q)
        doctor_status = result.fetchone()
    
    if not doctor_status:
        ret["status"] = "error"
        ret["message"] = "Doctor Inactive"
        return ret, 400
     

    doc_lookup_q = text(f"SELECT Doctor_ID, Days_Available FROM Slots WHERE Doctor_ID = '{Doctor_ID}' AND '{Current_Date}' BETWEEN Start_Date AND End_Date")
    with app.app_context():
        result = db.session.execute(doc_lookup_q)
        doctors = result.fetchone() 
    
    if not doctors:
        ret["status"] = "error"
        ret["message"] = "Doctor Currently Unavailable"
        return ret, 400
    
    ret["Doctor_ID"] = doctors[0]
    ret["Availabliity"] = json.loads(doctors[1])

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
    