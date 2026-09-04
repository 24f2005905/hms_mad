import json
import os 
import jwt
import uuid
import bcrypt
import psycopg2
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text,exc,inspect
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
    "user_id", "email_id","sex","first_name", "last_name", 
    "user_type", "phone_number","user_profile",
    "password","date_of_birth","address"
]
Valid_Days_Of_Week = [
    "mon", "tue", "wed", "thu", "fri", "sat", "sun"
]

Valid_Appt_Status = [
    "SCHEDULED", "COMPLETED", "CANCELLED"
]

def hash_password(password: str) -> str:
    cost = 14
    salted = bcrypt.gensalt(rounds=cost)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salted)
    return hashed.decode("utf-8")

def verify_password(password: str, pwd_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), pwd_hash.encode("utf-8"))
    except ValueError:
        # Invalid hash format, treat as mismatch
        return False

def init_db(ddl_path,table_name="users"):
    db_f_name = ddl_path.removeprefix("../sql/") 
    #Check whether the database is already initialized
    with app.app_context():
        inspector = inspect(db.engine)
        if inspector.has_table(table_name):
            print("Database already initialized")
            return 0
    
        print(f"Creating the DB {db_f_name}")
        # Create the SQL Lite using Alchemy
        sql_script = open(ddl_path,'r').read() 
   
        # Run the sql script
        with db.engine.begin() as conn:
            conn.execute(text(sql_script))

        print("Database successfully initialized")
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

    if "user_id" not in req_json or "password" not in req_json:
        return {"status":"error", "message":"Invalid request"}, 400
    
    User_ID = req_json["user_id"]
    Password = req_json["password"]

    query = text("SELECT user_type, password, user_status FROM users WHERE user_id = :user_id and user_status = 'ACTIVE'")
    with app.app_context():
        result = db.session.execute(query,{"user_id": User_ID})
        details = result.fetchone()
        if details:
            Role = details[0]
            pwd_hash = details[1] #Fetch password corresponding to User_ID
            
    #Password verification
    if not pwd_hash:
        return {"status":"error", "message":"Login Failed"}, 401
    else:
        if not verify_password(Password, pwd_hash):
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

@app.route("/hms/user/check-password", methods=["POST"])
@auth_wrapper
def Check_Password(auth_args):
    ret = {"status": "success"}
    # Check Auth
    if not auth_args['auth_token']:
        ret["status"] = "error"
        ret["message"] = auth_args["auth_err"]
        return ret, 401
    auth_token = auth_args['auth_token']

    # Get the request body
    req_json = request.get_json()

    if "user_id" not in req_json or "password" not in req_json:
        return {"status":"error", "message":"Invalid request"}, 400
    
    User_ID = req_json["user_id"]
    Password = req_json["password"]

    if auth_token['user'] != User_ID:
        return {"status":"error", "message":"Unauthorized request"}, 403

    query = text("SELECT user_type, password, user_status FROM users WHERE user_id = :user_id and user_status = 'ACTIVE'")
    with app.app_context():
        result = db.session.execute(query,{"user_id": User_ID})
        details = result.fetchone()
        if details:
            pwd_hash = details[1] #Fetch password corresponding to User_ID
    
    #Password verification
    if not pwd_hash:
        return {"status":"error", "message":"Login Failed"}, 401
    else:
        if not verify_password(Password, pwd_hash):
            return {"status":"error", "message":"Login Failed"}, 401
    
    return {
        "status":"succeess",
        "User_ID": User_ID
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
    if "first_name" not in req_json or \
        "user_type" not in req_json or \
        "sex" not in req_json or \
        "phone_number" not in req_json or \
        "password" not in req_json :
        ret["status"] = "error"
        ret["message"] = "Invalid request: Missing Mandatory Fields"
        return ret, 400
    
    # Check for valid User_Type
    if req_json["user_type"] not in Valid_User_Types:
        ret["status"] = "error"
        ret["message"] = f"Invalid User Type: {req_json['user_type']}"
        return ret, 400
    
    User_Type = req_json["user_type"]
    #Check for valid date of birth
    try:
        DOB = datetime.strptime(req_json["date_of_birth"],'%Y-%m-%d').date()
        if DOB > date.today():
            raise Exception("DOB in future")
    except:
        ret["status"] = "error"
        ret["message"] = "Invalid DOB Format"
        return ret, 400
    

    # Generate an ID: [P/A/D]-YYYY-MM-DD-[SNO]
    # Query for all User IDs for partial match
    query_1 = text("SELECT user_id FROM users WHERE user_id LIKE :partial_match ORDER BY id DESC")
    partial_match = f'{User_Type[0]}-{date.today().strftime("%Y-%m-%d")}-'
    serial_no = 1
    with app.app_context():
        result = db.session.execute(query_1,{"partial_match": partial_match+'%' })
        matches = result.fetchone()
    if matches: 
        serial_no = int(matches[0].split('-')[-1]) + 1
    User_ID = f"{partial_match}{serial_no:03d}"

    # Now insert the user
    query_2 = text ('INSERT INTO users '\
        '(user_id,email_id, sex,date_of_birth, address, first_name, last_name, ' \
        'user_type, phone_number, user_profile, password) ' \
        'VALUES (:User_ID,:Email_ID, :Sex ,:Date_Of_Birth,' \
        ':Address, :First_Name, :Last_Name, :User_Type,' \
        ':Phone_Number, :User_Profile, :Password)')
    query_2_dict = {
        "User_ID": User_ID,
        "Email_ID": req_json.get("email_id", ""),
        "Sex": req_json["sex"],
        "Date_Of_Birth": req_json.get("date_of_birth",""),
        "Address": req_json.get("address",""),
        "First_Name": req_json["first_name"],
        "Last_Name": req_json.get("last_name",""),
        "User_Type": User_Type,
        "Phone_Number": req_json["phone_number"],
        "User_Profile": json.dumps(req_json.get("user_profile",{})),
        "Password": hash_password(req_json["password"])
    }
    with app.app_context():
         result = db.session.execute(query_2,query_2_dict)
         db.session.commit()
        
    ret["user_id"] = User_ID
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
    for key in ['user_id','email_id','phone_number','first_name','last_name','user_type']:
        if key in param_json:
            match_clauses.append(f"LOWER({key}) LIKE LOWER('%{param_json[key]}%')")
    query = "SELECT * FROM users "
    if len(match_clauses):
        query += " WHERE "
        query += " AND ".join(match_clauses)

    if 'user_status' in param_json:
        query += f" AND user_status = '{param_json['user_status']}' "
        
    with app.app_context():
        result = db.session.execute(text(query))
        rows = result.fetchall() 
    
    user_details = []
    for row_ent in rows:
        row_dict = (dict(row_ent._mapping))
        row_dict.pop('password')
        row_dict.pop('id')
        if auth_token['role'] == 'ADMIN' or \
            auth_token['role'] == 'DOCTOR' and row_dict['User_ID'][0] == 'P' and \
                 row_dict['user_status'] == 'ACTIVE' or \
            auth_token['user'] == row_dict['user_id']:
            row_dict['user_profile'] = json.loads(row_dict['user_profile'])
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
    if 'user_id' not in req_json:
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
    query_check = f"SELECT user_id from users WHERE user_id = '{req_json['user_id']}';"
    with app.app_context():
        result = db.session.execute(text(query_check))
        rows = result.fetchall()
    
    if len(rows) != 1:
        ret["status"] = "error" 
        ret["message"] = "User Not Found"
        return ret, 400

    query = "UPDATE users SET "
    updates = []

    for column_name in req_json:
        if column_name not in Valid_User_Column:
            ret["status"] = "error" 
            ret["message"] = "Invalid Attribute"
            return ret, 400
        
        if column_name == 'user_id':
            continue 
        if column_name == 'date_of_birth':
            #Check for valid date of birth
            try:
                DOB = datetime.strptime(req_json["date_of_birth"],'%Y-%m-%d').date()
                
                if DOB > date.today():
                    raise Exception("DOB in future")
            except:
                ret["status"] = "error"
                ret["message"] = "Invalid DOB Format"
                return ret, 400
            
        column_data = (req_json[column_name] \
                if column_name != "password" else \
                    hash_password(req_json[column_name])) if \
            column_name != "user_profile" else \
            json.dumps(req_json[column_name])
        updates.append(f"{column_name} = '{column_data}'")
        
    
    if not updates:
        ret["status"] = "error" 
        ret["message"] = "No field to update"
        return ret, 400

    query += ",".join(updates)
    query += f" WHERE user_id = '{req_json['user_id']}';"

    with app.app_context():
        result = db.session.execute(text(query))
        db.session.commit()
    
    if result.rowcount != 1:
        ret["status"] = "error" 
        ret["message"] = "Failed to update"
        return ret, 500
    
    ret["user_id"] = req_json["user_id"]
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
    if 'user_id' not in param_json:
        ret["status"] = "error"
        ret["message"] = "User ID Not Provided"
        return ret, 400
    
    User_ID = param_json["user_id"]
   
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
    query_1 = f"SELECT user_id FROM users WHERE user_id = '{User_ID}';"
    with app.app_context():
        result = db.session.execute(text(query_1))
        rows = result.fetchall() 
   
    if len(rows) != 1:
        ret["status"] = "error" 
        ret["message"] = "User Not Found"
        return ret, 400
    
    #Query for deletion
    query =  f"UPDATE users SET user_status = 'INACTIVE' WHERE user_id = '{User_ID}';"
    with app.app_context():
        result = db.session.execute(text(query))
        db.session.commit()
    ret["user_id"] = User_ID 
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
    if "speciality" not in req_json:
        ret["status"] = "error"
        ret["message"] = "Invalid request: Missing Mandatory Fields"
        return ret, 400 
    
  
    #Generate Dept_ID : Dept-001 
    partial_match = 'Dept-'
    serial_no = 1 
    query = text("SELECT dept_id FROM departments WHERE dept_id LIKE :partial_match ORDER BY id DESC")
    with app.app_context():
        result = db.session.execute(query,{"partial_match": partial_match+'%' })
        matches = result.fetchone()
    if matches: 
        serial_no = int(matches[0].split('-')[-1]) + 1
    Dept_ID = f"{partial_match}{serial_no:03d}"

    # Updating Database 
    query_1 = text("INSERT INTO departments  " \
    "(dept_ID, speciality, details) VALUES "\
    "(:Dept_ID, :Speciality, :Details)")

    query_1_dict = {"Dept_ID": Dept_ID, "Speciality": req_json["speciality"], "Details": req_json.get("details","")}
    
    with app.app_context():
        try:
            result = db.session.execute(query_1,query_1_dict)
            db.session.commit()
        except exc.IntegrityError:
            ret["status"] = "error"
            ret["message"] = f"Department {req_json['speciality']} already exists."
            return ret, 400
        
    ret["dept_id"] = Dept_ID
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
    for key in ["dept_id","speciality"]:
        if key in param_json:
            match_clauses.append(f"LOWER({key}) LIKE LOWER('%{param_json[key]}%')")
    
    query = "SELECT * FROM departments"
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
    if 'dept_id' not in param_json:
        ret["status"] = "error"
        ret["message"] = "Department ID Not Provided"
        return ret, 400
    
    Dept_ID = param_json["dept_id"]

    #Enforcing Roles
    if auth_token['role'] != 'ADMIN':
        ret["status"] = "error" 
        ret["message"] = "Delete Unauthorized"
        return ret, 403 

    #Ensuring Department Exists
    query_1 = f"SELECT dept_id FROM departments WHERE dept_id = '{Dept_ID}';"
    with app.app_context():
        result = db.session.execute(text(query_1))
        rows = result.fetchall()
    
    if len(rows) != 1:
        ret["status"] = "error" 
        ret["message"] = "Department Not Found"
        return ret, 400

    query_2 = f"DELETE FROM departments WHERE dept_id = '{Dept_ID}';"
    with app.app_context():
        result = db.session.execute(text(query_2))
        db.session.commit()
    ret["dept_id"] = Dept_ID 
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
    if "doctor_id" not in req_json or \
        "days_available" not in req_json or \
        "start_date" not in req_json or \
        "end_date" not in req_json:
        ret["status"] = "error"
        ret["message"] = "Invalid request: Missing Mandatory Fields"
        return ret, 400 
    
    #Enforcing Role 
    if auth_token['role'] == 'PATIENT' or \
        (auth_token['role'] == 'DOCTOR' and auth_token['user'] != req_json["doctor_id"]):
        ret["status"] = "error"
        ret["message"] = "Unauthorized"
        return ret, 400
    
    #Check Valid User 
    query_1 = "SELECT user_id FROM users " \
        f"WHERE user_id = '{req_json['doctor_id']}' AND " \
        "user_status = 'ACTIVE'"
    with app.app_context():
        result = db.session.execute(text(query_1))
        rows = result.fetchone()
    
    if len(rows) != 1 :
        ret["status"] = "error"
        ret["message"] = "Invalid User"
        return ret, 400
    
    #Check valid date format
    try:
        Start_Date = datetime.strptime(req_json["start_date"],'%Y-%m-%d').date()
        End_Date = datetime.strptime(req_json["end_date"],'%Y-%m-%d').date()
        if End_Date < Start_Date:
             ret["status"] = "error"
             ret["message"] = "Invalid Date Range"
             return ret, 400
    except:
        ret["status"] = "error"
        ret["message"] = "Invalid Date Format"
        return ret, 400
    
    #Define valid day of week 
    for day in req_json["days_available"]:
        if day.lower() not in Valid_Days_Of_Week:
            ret["status"] = "error"
            ret["message"] = "Invalid Day Of Week"
            return ret, 400

   #Check existence of Doctor_ID
    query_2 = text("SELECT doctor_id,start_date,end_date FROM slots WHERE doctor_id = :Doctor_ID")
    with app.app_context():
        result = db.session.execute(query_2,{"Doctor_ID": req_json["doctor_id"]})
        rows = result.fetchone()
   
   #If Doctor_ID exists, update row instead
    if rows:
        Old_Start_Date = rows[1]
        Old_End_Date = rows[2]
        
        open_app_query = "SELECT appointment_id FROM appointments  " \
            "WHERE appointment_status = 'SCHEDULED' AND " \
            f"doctor_id = '{req_json['doctor_id']}' AND " \
            f"(appointment_date BETWEEN '{Old_Start_Date}' AND '{Old_End_Date}');"
        
        with app.app_context():
            open_appointments = db.session.execute(text(open_app_query))
            rows = open_appointments.fetchall()

        if len(rows):
            ret["status"] = "error" 
            ret["message"] = "Clear Existing Appointments before updating slots"
            return ret, 400 

        # There are no existing appointments. Delete the old Slot
        del_old_slot_q = text(f"DELETE from slots WHERE doctor_id = '{req_json['doctor_id']}'")
        with app.app_context():
            del_old_slots = db.session.execute(del_old_slot_q)
            db.session.commit()
        
        if del_old_slots.rowcount != 1:
            ret["status"] = "error" 
            ret["message"] = "Error Deleting Old Slot"
            return ret, 500 
            
       

    #Creating new slot      
    query_3 = text("INSERT INTO slots  " \
    "(doctor_id, days_available, start_date, end_date) VALUES "\
    "(:Doctor_ID, :Days_Available, :Start_Date, :End_Date)")

    query_3_dict = {
        "Doctor_ID": req_json["doctor_id"], "Days_Available": json.dumps(req_json["days_available"]), 
        "Start_Date": req_json["start_date"], "End_Date": req_json["end_date"]
        }
    
    with app.app_context():
        result = db.session.execute(query_3,query_3_dict)
        db.session.commit()

    ret["doctor_id"] = req_json['doctor_id']
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
    Doctor_ID = param_json["doctor_id"]

    #Check Doctor_Status 
    doctor_status_q = text("SELECT user_status FROM users " \
                          f"WHERE user_id = '{Doctor_ID}' AND user_status = 'ACTIVE'")
    with app.app_context():
        result = db.session.execute(doctor_status_q)
        doctor_status = result.fetchone()
    
    if not doctor_status:
        ret["status"] = "error"
        ret["message"] = "Doctor Inactive"
        return ret, 400
     

    doc_lookup_q = text(f"SELECT start_date, end_date, days_available FROM slots WHERE doctor_id = '{Doctor_ID}'")
    with app.app_context():
        result = db.session.execute(doc_lookup_q)
        slots = result.fetchone() 
    
    if not slots:
        ret["status"] = "error"
        ret["message"] = "Doctor Currently Unavailable"
        return ret, 400
    ret["Slot"] = {
        "start_date": slots[0],
        "end_date": slots[1],
        "days_available": json.loads(slots[2])
    }
    

    return ret, 200

@app.route("/hms/departments/assign", methods=["POST"])
@auth_wrapper
def Assign_Doctor(auth_args):
    ret = {"status": "success"}
    # Check Auth
    if not auth_args['auth_token']:
        ret["status"] = "error"
        ret["message"] = auth_args["auth_err"]
        return ret, 401
    auth_token = auth_args['auth_token']

    # Get the request body
    req_json = request.get_json()

    #Enforce Roles 
    if auth_token['role'] != 'ADMIN':
        ret["status"] = "error"
        ret["message"] = "Unauthorized Action"
        return ret, 403 

    #Check Mandatory Fields
    if "doctor_id" not in req_json or \
        "dept_id" not in req_json or \
        "dept_position" not in req_json :
        ret["status"] = "error"
        ret["message"] = "Invalid request: Missing Mandatory Fields"
        return ret, 400
    
    Doctor_ID = req_json["doctor_id"]
    Dept_ID = req_json["dept_id"]
    Dept_Position = req_json["dept_position"]

    #Check existence of user and whether the user is a doctor and active
    user_search= "SELECT user_id FROM users " \
        f"WHERE user_id = '{req_json['doctor_id']}' AND " \
        "user_status = 'ACTIVE' and user_type = 'DOCTOR'"
    with app.app_context():
        result = db.session.execute(text(user_search))
        rows = result.fetchone()
    
    if not rows :
        ret["status"] = "error"
        ret["message"] = "Invalid Doctor ID"
        return ret, 400
    
    #Check existence of department
    dept_search= "SELECT dept_id FROM departments " \
        f"WHERE dept_id = '{Dept_ID}';"
    with app.app_context():
        result = db.session.execute(text(dept_search))
        rows = result.fetchone()
    
    if not rows :
        ret["status"] = "error"
        ret["message"] = "Department does not exist"
        return ret, 400

    #Only one HOD in department
    if Dept_Position == 'HOD':
        hod_search = text("SELECT dept_position FROM doctor_dept "\
                        f"WHERE dept_id = '{Dept_ID}' AND dept_position = 'HOD';")
        with app.app_context():
            result = db.session.execute(hod_search)
            rows = result.fetchall()
        
        if len(rows) > 0:
             ret["status"] = "error"
             ret["message"] = "HOD for department already exists"
             return ret, 400
        
    #Check if doctor already assigned
    doctor_search = text("SELECT doctor_id, dept_id, dept_position from doctor_dept "\
                         f"WHERE doctor_id = '{Doctor_ID}' AND dept_id = '{Dept_ID}'")
    with app.app_context():
        result = db.session.execute(doctor_search)
        rows = result.fetchone()
    
    if rows:
        Current_Position = rows[2]
        if Current_Position == Dept_Position:
            ret["status"] = "error"
            ret["message"] = "Doctor already assigned to department"
            return ret, 400
        # Delete the Doctor-Dept entry and insert new one
        doctor_del = text("DELETE FROM doctor_dept WHERE " \
                        f"doctor_id = '{Doctor_ID}' and dept_id = '{Dept_ID}';")
        with app.app_context():
            result = db.session.execute(doctor_del)
            db.session.commit()
        if result.rowcount == 0:
            ret["status"] = "error"
            ret["message"] = "DB Update error on delete"
            return ret, 500
        
    doctor_assign = text("INSERT INTO doctor_dept(doctor_id,dept_id, dept_position) VALUES "\
                         f"('{Doctor_ID}', '{Dept_ID}', '{Dept_Position}');" )
    with app.app_context():
            result = db.session.execute(doctor_assign)
            db.session.commit()
    
    ret["doctor_id"] = Doctor_ID
    ret["dept_id"] = Dept_ID 
    return ret, 200
    
@app.route("/hms/departments/unassign", methods=["DELETE"])
@auth_wrapper
def Unassign_Doctor(auth_args):
    ret = {"status": "success"}
    # Check Auth
    if not auth_args['auth_token']:
        ret["status"] = "error"
        ret["message"] = auth_args["auth_err"]
        return ret, 401
    auth_token = auth_args['auth_token']

    #Get parameters
    param_json = request.args.to_dict()
    
    #Check for mandatory fields₹
    if "doctor_id" not in param_json or "dept_id" not in param_json:
        ret["status"] = "error"
        ret["message"] = "missing mandatory fields"
        return ret, 400

    Doctor_ID = param_json["doctor_id"]
    Dept_ID = param_json["dept_id"]
    
    #Enforce Roles 
    if auth_token['role'] != 'ADMIN':
        ret["status"] = "error"
        ret["message"] = "Unauthorized Action"
        return ret, 403 
    
    #Check existence of user and whether the user is a doctor 
    user_search= "SELECT user_id FROM users " \
        f"WHERE user_id = '{param_json['doctor_id']}' AND " \
        "user_type = 'DOCTOR'"
    with app.app_context():
        result = db.session.execute(text(user_search))
        rows = result.fetchone()
    
    if not rows :
        ret["status"] = "error"
        ret["message"] = "Invalid Doctor ID"
        return ret, 400

    #Check if doctor already assigned
    doctor_search = text("SELECT doctor_id, dept_id, dept_position from doctor_dept "\
                         f"WHERE doctor_id = '{Doctor_ID}' AND dept_id = '{Dept_ID}'")
    with app.app_context():
        result = db.session.execute(doctor_search)
        rows = result.fetchone()
    
    if not rows:
        ret["status"] = "error"
        ret["message"] = "Doctor does not belong to this department."
        return ret, 400
    
    #Unassign Doctor Query
    doctor_del = text("DELETE FROM doctor_dept WHERE " \
                        f"doctor_id = '{Doctor_ID}' and dept_id = '{Dept_ID}';")
    with app.app_context():
            result = db.session.execute(doctor_del)
            db.session.commit()
    if result.rowcount == 0:
            ret["status"] = "error"
            ret["message"] = "DB Update error on delete"
            return ret, 500
    
    ret["doctor_id"] = Doctor_ID 
    return ret, 200 

@app.route("/hms/departments/doctor-lookup", methods=["GET"])
@auth_wrapper
def Doctor_Lookup(auth_args):
    ret = {"status": "success"}
    # Check Auth
    if not auth_args['auth_token']:
        ret["status"] = "error"
        ret["message"] = auth_args["auth_err"]
        return ret, 401
    
    #Get parameters
    param_json = request.args.to_dict()
    
    #Generate lookup query
    match_clauses = []
    for key in ['user_id','specialities','first_name','last_name']:
        if key in param_json:
            match_clauses.append(f"LOWER({key}) LIKE LOWER('%{param_json[key]}%')")
    
    query = "SELECT * FROM doctor_lookup "

    if len(match_clauses):
        query += " WHERE "
        query += " AND ".join(match_clauses)

    print(query)
    with app.app_context():
        doctor_lookup = db.session.execute(text(query))
        doctors = doctor_lookup.fetchall() 
    
    doctor_details = []
    for doctor in doctors:
        doctor_dict = (dict(doctor._mapping))
        doctor_details.append(doctor_dict)
    ret['doctordept_details'] = doctor_details
    return ret, 200

@app.route("/hms/appointment/create", methods=["POST"])
@auth_wrapper
def Appointment_Create(auth_args):
    ret = {"status": "success"}
    # Check Auth
    if not auth_args['auth_token']:
        ret["status"] = "error"
        ret["message"] = auth_args["auth_err"]
        return ret, 401
    
    # Get the request body
    req_json = request.get_json() 
    
    # Check for Mandatory Fields
    if "patient_id" not in req_json or \
        "doctor_id" not in req_json or \
        "appointment_date" not in req_json or \
        "appointment_time" not in req_json :
        ret["status"] = "error"
        ret["message"] = "Invalid request: Missing Mandatory Fields"
        return ret, 400
    
    auth_token = auth_args['auth_token']
    Doctor_ID = req_json["doctor_id"]
    Patient_ID = req_json["patient_id"]
    Appointment_Date = req_json["appointment_date"]
    Appointment_Time = req_json["appointment_time"]

    
    #Check Role - ADMIN:Everyone, PATIENT: Himself, DOCTOR: None 
    if auth_token['role'] == 'DOCTOR' or  \
            (auth_token['role'] == 'PATIENT' and auth_token['user'] != Patient_ID):
        ret["status"] = "error"
        ret["message"] = "Unauthorized Action"
        return ret, 403

    #Check Doctor Status and Patient Status
    doctor_search = text("SELECT user_status from users " \
            f"WHERE user_id = '{Doctor_ID}' AND user_status = 'ACTIVE';")
    patient_search = text("SELECT user_status from users " \
            f"WHERE user_id = '{Patient_ID}' AND user_status = 'ACTIVE';")
    
    with app.app_context():
        doc_result = db.session.execute(doctor_search)
        pat_result = db.session.execute(patient_search)
        doctor = doc_result.fetchone() 
        patient = pat_result.fetchone()
    
    if ((not doctor) or (not patient)):
        ret["status"] = "error"
        ret["message"] = "Either Doctor or Patient does not exist"
        return ret, 400
    
    #Check for appointment time  format 
    try: 
        _ = datetime.strptime(Appointment_Time, "%H:%M")
        hour,min = Appointment_Time.split(':')
        hour = int(hour)
        min = int(min)

        if (not (9 <= hour < 12) and not(14 <= hour < 17)) or \
            (not (min % 15 == 0)):
            ret["status"] = "error"
            ret["message"] = "Invalid Time Slot"
            return ret, 400
        
    except ValueError:
         ret["status"] = "error"
         ret["message"] = "Invalid Appointment_Time"
         return ret, 400
    

    #Check Appt Date is in valid format
    try:
        _ = datetime.strptime(Appointment_Date,'%Y-%m-%d').date()
    except:
        ret["status"] = "error"
        ret["message"] = "Invalid Date Format"
        return ret, 400
    
    #Lookup Slot to see if Appt_Date is in date range
    slot_lookup = text("SELECT days_available FROM slots "\
        f"WHERE doctor_id = '{Doctor_ID}' AND "\
        f"('{Appointment_Date}' BETWEEN start_date AND end_date) ")
    with app.app_context():
        slot_search = db.session.execute(slot_lookup)
        details = slot_search.fetchone()
    
    if not details:
        ret["status"] = "error"
        ret["message"] = "Slots Unavailable"
        return ret, 400

    Days_Available = [d.lower() for d in  json.loads(details[0])]
    # Figure out day of week from appt date and check in days available
    day_of_week = datetime.strptime(Appointment_Date, "%Y-%m-%d").strftime("%a").lower()
    if day_of_week not in Days_Available:
        ret["status"] = "error"
        ret["message"] = f"Doctor not available on {day_of_week.upper()}"
        return ret, 400

    #Check for existing appoinments in appointment table for Doctor
    appt_search_q = text("SELECT appointment_id FROM appointments " \
        f"WHERE appointment_date = '{Appointment_Date}' AND " \
        f"appointment_time = '{Appointment_Time}' AND doctor_id = '{Doctor_ID}' " \
        "AND appointment_status = 'SCHEDULED'")
    
    with app.app_context():
        appt_search = db.session.execute(appt_search_q)
        details = appt_search.fetchone()
    
    if details:
        ret["status"] = "error"
        ret["message"] = "Appointment Slot Taken"
        return ret, 400
    
    #Check for existing appoinments in appointment table for Patient
    appt_search_q = text("SELECT appointment_id FROM appointments " \
        f"WHERE appointment_date = '{Appointment_Date}' AND " \
        f"appointment_time = '{Appointment_Time}' AND patient_id = '{Patient_ID}' " \
        "AND appointment_status = 'SCHEDULED'")
    
    with app.app_context():
        appt_search = db.session.execute(appt_search_q)
        details = appt_search.fetchone()
    
    if details:
        ret["status"] = "error"
        ret["message"] = "Patient Slot not available"
        return ret, 400
    
    #Generate Appointment_ID 
    Appointment_ID = str(uuid.uuid4())
    appt_create_q = text("INSERT INTO appointments VALUES " \
        f"('{Appointment_ID}', '{Patient_ID}', " \
        f"'{Doctor_ID}', '{Appointment_Date}', '{Appointment_Time}', 'SCHEDULED')")

    with app.app_context():
        appt_create = db.session.execute(appt_create_q)
        db.session.commit()
    
    if appt_create.rowcount != 1:
        ret["status"] = "error"
        ret["message"] = "Unable to create appointment."
        return ret, 500
    
    ret["appointment_id"] = Appointment_ID 
    return ret, 200

@app.route("/hms/appointments/lookup", methods=["GET"])
@auth_wrapper
def Appointment_Lookup(auth_args):
    ret = {"status": "success"}
    # Check Auth
    if not auth_args['auth_token']:
        ret["status"] = "error"
        ret["message"] = auth_args["auth_err"]
        return ret, 401
    auth_token = auth_args['auth_token']
    
    #Get parameters
    param_json = request.args.to_dict()
    
    if 'appointment_status' not in param_json:
        param_json['appointment_status'] = 'SCHEDULED'
        
    elif param_json['appointment_status'] == 'ALL':
        param_json.pop('appointment_status')
    

    User_ID = auth_token['user']
    User_Role = auth_token['role']

    match_clauses = []

    for key in ['appointment_id','patient_id','doctor_id','appointment_date','appointment_status']:
        if key in param_json:
            # Enforce date format
            try:
                if key == 'appointment_date':
                    _ = datetime.strptime(param_json[key],'%Y-%m-%d').date()
                if key == 'appointment_status' and \
                    param_json[key] not in Valid_Appt_Status:
                    raise Exception("Invalid Appointment Status")
            except:
                ret["status"] = "error"
                ret["message"] = "Invalid Search parameter"
                return ret, 400
            
            match_clauses.append(f"{key} = '{param_json[key]}'")
    
    if User_Role == 'PATIENT' and 'patient_id' not in param_json:
        match_clauses.append(f"patient_id = '{User_ID}'")
    elif User_Role == 'DOCTOR' and 'doctor_id' not in param_json:
        match_clauses.append(f"doctor_id = '{User_ID}'")
    else:
        if "patient_id" not in param_json and \
            "doctor_id" not in param_json and \
            "appointment_date" not in param_json and \
            "appointment_id" not in param_json and \
            "appointment_status" not in param_json:
            ret["status"] = "error"
            ret["message"] = "ADMIN must use one of the filters"
            return ret, 400
        
    query = "SELECT * FROM appointment_lookup "
    if len(match_clauses):
        query += " WHERE "
        query += " AND ".join(match_clauses)
        query += " ORDER BY appointment_date"
 
    with app.app_context():
        result = db.session.execute(text(query))
        rows = result.fetchall() 
    
    appointment_details = []
    for appt in rows:
        row_dict = (dict(appt._mapping))
        appointment_details.append(row_dict)
    
    ret["appointment_details"] = appointment_details
    return ret, 200 

@app.route("/hms/appointment/update", methods=["PUT"])
@auth_wrapper
def Appointment_Update(auth_args):
    ret = {"status": "success"}
    # Check Auth
    if not auth_args['auth_token']:
        ret["status"] = "error"
        ret["message"] = auth_args["auth_err"]
        return ret, 401
    auth_token = auth_args['auth_token']
    
    User_ID = auth_token['user']
    User_Role = auth_token['role']
    
    # Get the request body
    param_json = request.args.to_dict()

    #Check mandatory fields
    if ("appointment_id" not in param_json and \
            "patient_id" not in param_json and \
            "doctor_id" not in param_json) or \
        "appointment_status" not in param_json or \
        param_json["appointment_status"] not in ['COMPLETED','CANCELLED']:
        ret["status"] = "error"
        ret["message"] = "Invalid Parameters"
        return ret, 400
    
    Appointment_ID = param_json.get("appointment_id", None)
    Appointment_Status = param_json["appointment_status"]

    # Build match clauses
    match_clauses = []
    for key in ["appointment_id", "patient_id", "doctor_id"]:
        if key in param_json:
            match_clauses.append(f"{key} = '{param_json[key]}'")

    #Check Appointment Exists 
    appt_query = "SELECT patient_id, doctor_id FROM appointments WHERE " \
        "appointment_status = 'SCHEDULED' " 
    
    if len(match_clauses):
        appt_query += ' AND '.join(match_clauses) \
            if len(match_clauses) > 1 else f" AND {match_clauses[0]}"

    if Appointment_Status == 'COMPLETED':
        appt_query += " AND appointment_date <= CURRENT_DATE"
    
    with app.app_context():
        result = db.session.execute(text(appt_query))
        row = result.fetchone()
    
    if not row:
        ret["status"] = "error"
        ret["message"] = "Appointment Not Found"
        return ret, 400
    
    #Enforce Role
    if (User_Role == 'PATIENT' and \
            (User_ID != row[0] or Appointment_Status != "CANCELLED")) or \
        (User_Role == 'DOCTOR' and \
            (User_ID != row[1] or Appointment_Status not in \
                ["COMPLETED", "CANCELLED"])) or \
        (User_Role == 'ADMIN' and \
            Appointment_Status != 'CANCELLED'):
        ret["status"] = "error"
        ret["message"] = "Appointment Update Unauthorized"
        return ret, 403
    
    #Update the database 
    update_query = "UPDATE appointments SET " \
        f"appointment_status = '{Appointment_Status}' WHERE "
    
    if len(match_clauses):
        update_query += ' AND '.join(match_clauses) \
            if len(match_clauses) > 1 else f"{match_clauses[0]}"
    
    with app.app_context():
        result = db.session.execute(text(update_query))
        db.session.commit()
    
    if result.rowcount < 1:
        ret["status"] = "error"
        ret["message"] = "Appointment Update Failed"
        return ret, 500

    ret["appointment_id"] = Appointment_ID

    return ret, 200

@app.route("/hms/treatments/upload", methods=["POST"])
@auth_wrapper
def Treatment_Upload(auth_args):
    ret = {"status": "success"}
    # Check Auth
    if not auth_args['auth_token']:
        ret["status"] = "error"
        ret["message"] = auth_args["auth_err"]
        return ret, 401
    auth_token = auth_args['auth_token']
    
    # Get the request body
    req_json = request.get_json()

    # Check for Mandatory Fields
    if "appointment_id" not in req_json or \
        "notes" not in req_json:
        ret["status"] = "error"
        ret["message"] = "Invalid request: Missing Mandatory Fields"
        return ret, 400
    
    #Enforce role 
    if auth_token['role'] != 'DOCTOR':
        ret["status"] = "error"
        ret["message"] = "Unauthorized Action"
        return ret, 403
    
    Appointment_ID = req_json["appointment_id"]
    

    #Check if Doctor_ID matches Doctor_ID in appointments AND If appointment exists
    appt_search_q = text ("SELECT doctor_id FROM appointments " \
            f"WHERE appointment_id = '{Appointment_ID}' AND appointment_status = 'SCHEDULED'" \
            "AND appointment_date <= CURRENT_DATE;")
    
    with app.app_context():
         appt_search = db.session.execute(appt_search_q)
         appt = appt_search.fetchone()
    
    if not appt:
        ret["status"] = "error"
        ret["message"] = "Appointment does not Exist"
        return ret, 400
    
    if appt[0] != auth_token['user']:
        ret["status"] = "error"
        ret["message"] = "Unauthorized Action"
        return ret, 403   
    
    #Check if treatment already exists
    treatment_search_q = text ("SELECT appointment_id FROM treatments " \
            f"WHERE appointment_id = '{Appointment_ID}';")
    
    with app.app_context():
         treat_search = db.session.execute(treatment_search_q)
         treat = treat_search.fetchone()
    
    if treat:
        ret["status"] = "error"
        ret["message"] = "Treatment already Exists"
        return ret, 400
    

    #Create Treatment query
    upload_query = text ('INSERT INTO treatments '\
        '(appointment_id, diagnosis, ' \
        'prescription, notes) ' \
        'VALUES (:Appointment_ID, ' \
        ':Diagnosis, :Prescription, ' \
        ':Notes);')
    upload_query_dict = {
        "Appointment_ID": Appointment_ID,
        "Diagnosis": req_json.get("diagnosis",""),
        "Prescription": req_json.get("prescription",""),
        "Notes": req_json.get("notes")
    }

    with app.app_context():
         db.session.execute(upload_query,upload_query_dict)
         db.session.commit()
        
    ret["appointment_id"] = Appointment_ID
    return ret, 200

@app.route("/hms/treatments/update", methods=["POST"])
@auth_wrapper
def Treatment_Update(auth_args):
    ret = {"status": "success"}
    # Check Auth
    if not auth_args['auth_token']:
        ret["status"] = "error"
        ret["message"] = auth_args["auth_err"]
        return ret, 401
    auth_token = auth_args['auth_token']

    # Get the request body
    req_json = request.get_json()
   
    #Checking for Mandatory Fields
    if 'appointment_id' not in req_json:
        ret["status"] = "error" 
        ret["message"] = "Appointment_ID not found"
        return ret, 400
    
    if 'diagnosis' not in req_json and \
        'prescription' not in req_json and \
            'notes' not in req_json:
        ret["status"] = "error" 
        ret["message"] = "No field to update"
        return ret, 400
    
    Appointment_ID = req_json["appointment_id"]
    
    #Enforce Role
    if auth_token['role'] != 'DOCTOR':
        ret["status"] = "error"
        ret["message"] = "Unauthorized Action"
        return ret, 403
    
    #Check if Doctor_ID matches Doctor_ID in appointments AND If appointment exists
    appt_search_q = text ("SELECT doctor_id FROM appointments " \
            f"WHERE appointment_id = '{Appointment_ID}' AND appointment_status = 'SCHEDULED'" \
            "AND appointment_date <= CURRENT_DATE;")
    
    with app.app_context():
         appt_search = db.session.execute(appt_search_q)
         appt = appt_search.fetchone()
    
    if not appt:
        ret["status"] = "error"
        ret["message"] = "Appointment does not Exist"
        return ret, 400
    
    if appt[0] != auth_token['user']:
        ret["status"] = "error"
        ret["message"] = "Unauthorized Action"
        return ret, 403  
    
    #Check if treatment already exists
    treatment_search_q = text ("SELECT appointment_id FROM treatments " \
            f"WHERE appointment_id = '{Appointment_ID}';")
    
    with app.app_context():
         treat_search = db.session.execute(treatment_search_q)
         treat = treat_search.fetchone()
    
    if not treat:
        ret["status"] = "error"
        ret["message"] = "Treatment does not exist"
        return ret, 400 
    
    # Creating update query

    update_fields = []
    for field in req_json:
        if field == 'appointment_id':
            continue
        update_data = req_json[field]
        update_fields.append(f"{field} = '{update_data}'")
    
    update_q = "UPDATE treatments SET "
    update_q += ','.join(update_fields)
    update_q += f" WHERE appointment_id = '{Appointment_ID}';"
    
    with app.app_context():
        update = db.session.execute(text(update_q))
        db.session.commit()
    
    if update.rowcount != 1:
        ret["status"] = "error" 
        ret["message"] = "Failed to update"
        return ret, 500
    
    ret["appointment_id"] = Appointment_ID
    return ret, 200

@app.route("/hms/treatments/lookup", methods=["GET"])
@auth_wrapper
def Treatment_Lookup(auth_args):
    ret = {"status": "success"}
    # Check Auth
    if not auth_args['auth_token']:
        ret["status"] = "error"
        ret["message"] = auth_args["auth_err"]
        return ret, 401
    auth_token = auth_args['auth_token']
    User_Role = auth_token['role']
    User_ID = auth_token['user']
    #Get parameters
    param_json = request.args.to_dict()

    match_clauses = []
    for key in ['appointment_id','doctor_id','patient_id','appointment_date']:
        if key in param_json:
            match_clauses.append(f"{key} = '{param_json[key]}'")

    if User_Role == 'PATIENT':
        match_clauses.append(f"patient_id = '{User_ID}'")
    elif User_Role == 'DOCTOR' and "Patient_ID" not in param_json:
        ret["status"] = "error"
        ret["message"] = "Doctor should provide Patient ID"
        return ret, 400
    
    if "patient_id" not in param_json and \
        "doctor_id" not in param_json and \
        "appointment_id" not in param_json and \
        "appointment_date" not in param_json:
        ret["status"] = "error"
        ret["message"] = "Must use one of the filters"
        return ret, 400
  
    query = "SELECT * FROM treatment_lookup "
    if len(match_clauses):
        query += " WHERE "
        query += " AND ".join(match_clauses)
        query += " ORDER BY appointment_date"
    
    print(query)
    with app.app_context():
        result = db.session.execute(text(query))
        rows = result.fetchall() 
    
    treatment_details = []
    for treatment in rows:
        row_dict = (dict(treatment._mapping))
        treatment_details.append(row_dict)
    
    ret["treatment_details"] = treatment_details
    return ret, 200
    
@app.route("/hms/slots/availability", methods=["GET"])
@auth_wrapper
def Available_Slots(auth_args):
    ret = {"status": "success"}
    # Check Auth
    if not auth_args['auth_token']:
        ret["status"] = "error"
        ret["message"] = auth_args["auth_err"]
        return ret, 401
    
    #Get parameters
    param_json = request.args.to_dict()

     # Check for Mandatory Fields
    if "doctor_id" not in param_json or \
        "appointment_date" not in param_json:
        ret["status"] = "error"
        ret["message"] = "Invalid request: Missing Mandatory Fields"
        return ret, 400
    
    Doctor_ID = param_json["doctor_id"]
    Appointment_Date = param_json["appointment_date"]

    #Creating Slots 9:00 - 12:00, 14:00-17:00
    Free_Slots = ["09:00", "09:15", "09:30", "09:45",
        "10:00", "10:15", "10:30", "10:45",
        "11:00", "11:15", "11:30", "11:45", 
        "14:00", "14:15", "14:30", "14:45", 
        "15:00", "15:15", "15:30", "15:45",
        "16:00", "16:15", "16:30", "16:45"]


    #Check Appt Date is in valid format
    try:
        _ = datetime.strptime(Appointment_Date,'%Y-%m-%d').date()
    except:
        ret["status"] = "error"
        ret["message"] = "Invalid Date Format"
        return ret, 400
    
    #Lookup Slot to see if Appt_Date is in date range
    slot_lookup = text("SELECT days_available FROM slots "\
        f"WHERE doctor_id = '{Doctor_ID}' AND "\
        f"('{Appointment_Date}' BETWEEN start_date AND end_date) ")
    with app.app_context():
        slot_search = db.session.execute(slot_lookup)
        details = slot_search.fetchone()
    
    if not details:
        ret["free_slots"] = []
        return ret, 200
   
    Days_Available = json.loads(details[0])
    # Figure out day of week from appt date and check in days available
    day_of_week = datetime.strptime(Appointment_Date, "%Y-%m-%d").strftime("%a").lower()
    if day_of_week not in [d.lower() for d in Days_Available]:
        ret["Free_Slots"] = []
        return ret, 200
    
    #Find Appointments already booked on Date
    appt_search_q = text("SELECT appointment_time FROM appointments "\
        f"WHERE appointment_date = '{Appointment_Date}' AND " \
        f"doctor_id = '{Doctor_ID}' AND appointment_status = 'SCHEDULED'")
 
    with app.app_context():
        appt_search = db.session.execute(appt_search_q)
        booked_slots = appt_search.fetchall()
    
    if not booked_slots:
        ret['free_slots'] = Free_Slots
        return ret, 200
    
    for i in range(0,len(booked_slots)):
        slot = booked_slots[i][0]
        if slot in Free_Slots:
            Free_Slots.remove(slot)
    
    ret['free_slots'] = Free_Slots
    return ret, 200

    
if __name__ == '__main__' :
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

    init_db(config_dict["ddl_path"],"users")

    app.run(host='0.0.0.0',debug = True , port = config_dict['port'])
    
