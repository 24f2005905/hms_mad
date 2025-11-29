import json
from flask import Flask, render_template, request, redirect, url_for
from jinja2 import FileSystemLoader
import requests
import uuid
import jwt
import json
from flask import session, flash
from functools import wraps
from datetime import datetime, timedelta, date

app = Flask(__name__)
app_url = None
session_dict = {}
valid_gender_str = {
	'M': 'Male',
	'F': 'Female'
}
my_auth_token = None

Free_Slots = ["09:00", "09:15", "09:30", "09:45",
        "10:00", "10:15", "10:30", "10:45",
        "11:00", "11:15", "11:30", "11:45", 
        "14:00", "14:15", "14:30", "14:45", 
        "15:00", "15:15", "15:30", "15:45",
        "16:00", "16:15", "16:30", "16:45"]

role_to_dash = {
    "ADMIN" : "admin_dashboard.html",
    "PATIENT": "patient_dashboard.html",
    "DOCTOR": "doctor_dashboard.html"
}
def gen_backend_token(user, password):
    # Generate auth token from backend
    login_dict = {
        "User_ID": user,
        "Password": password
    }
    http_resp = requests.post(app_url + '/hms/id/generate/token', json=login_dict, timeout=60)
    if http_resp.status_code != 200:
        flash("Login Failed","error")
        return redirect("/login")
    
    # Extract Auth Token and Save in session
    auth_token_str = http_resp.json().get('token', None)
    if not auth_token_str:
        flash("Login Failed","error")
        return redirect("/login")
    
    return auth_token_str

def calculate_age(dob_str):
    dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

def get_next_7_days():
    current_date = datetime.now()
    date_list = []
    for i in range(7):
       date_list.append(( current_date + timedelta(days = i + 1)).strftime('%d %B %Y'))
    return date_list

def session_wrapper(f):
    """ Session Wrapper Decorator"""
    @wraps(f)
    def sid_wrapper(*args, **kwargs):
        # Check for valid session
        sid = session.get('sid')
        my_session_dict = session_dict.get(sid, None)
        # TODO: Check for token expiry
        # Current time must be between 'iat' and 'exp'
        if my_session_dict:
            auth_token_str = my_session_dict["token"]
            try:
                _ = jwt.decode(auth_token_str, jwt_public_str, algorithms = ["RS256"])
            except Exception as e:
                my_session_dict = None 
                session_dict.pop(sid,None)
                session.clear()
        kwargs['sid'] = my_session_dict
        return f(*args, **kwargs)
    return sid_wrapper

@app.route('/register', methods=['GET', 'POST'])
@session_wrapper
def register(sid):
    if sid:
        return redirect("/dashboard")
    
    # Present the form for new user
    if request.method == 'GET':
        return render_template("register.html")
    
    headers = {
        "Authorization": my_auth_token
    }
    
    create_dict = {
    "First_Name": request.form.get('First_Name'),
    "Last_Name" : request.form.get('Last_Name',None),
    "Phone_Number" :request.form.get('Phone_Number'),
    "User_Type": "PATIENT",
    "Email_ID" : request.form.get('Email_ID'),
    "Sex" : request.form.get('Sex')[0].upper(),
    "Address" : request.form.get('Address',None),
    "Date_Of_Birth" :request.form.get('Date_Of_Birth'),
    "Password" : request.form.get('password'),
    "New_Password" : request.form.get('cnf_password')
    }

    user_create = requests.post(app_url + '/hms/user/create',json= create_dict, headers= headers, timeout=60)
    if user_create.status_code != 200:
        flash(f"Registration Failed{user_create.json().get('message')}","error")
        return redirect("/login")
    
    User_ID = user_create.json().get('User_ID')
    return render_template("register_success.html", User_ID = User_ID, User_Type=create_dict['User_Type'])

@app.route('/doctor_register', methods=['GET', 'POST'])
@session_wrapper
def Doctor_Register(sid):
    if not sid:
        return redirect("/login")
    
    headers = {
        "Authorization": sid['token']
    }

    # Present the form for new user
    if request.method == 'GET':
         #Specialisation Lookup
        spec_lookup = requests.get(app_url + '/hms/departments/lookup',headers=headers, timeout =60)
        departments = spec_lookup.json().get('department_details')
        specialisations = []
        for spec in departments:
            specialisations.append(spec["Speciality"]) 
        return render_template("doctor_register.html", user_token = sid, specialisations_list = specialisations)
    
    # Updating Database with User details
    User_Profile = {
        "Qualifications": request.form.get("Qualification",None),
        "Experience": request.form.get("Experience",None),
        "Expertise": request.form.get("Expertise",None),
        "Bio": request.form.get("Bio",None)

    }
    create_user_dict = {
    "First_Name": request.form.get('First_Name'),
    "Last_Name" : request.form.get('Last_Name',None),
    "Phone_Number" :request.form.get('Phone_Number'),
    "User_Type": "DOCTOR",
    "Email_ID" : request.form.get('Email_ID'),
    "Sex" : request.form.get('Sex')[0].upper(),
    "Address" : request.form.get('Address',None),
    "Date_Of_Birth" :request.form.get('Date_Of_Birth'),
    "Password" : request.form.get('password'),
    "New_Password" : request.form.get('cnf_password'),
    "User_Profile": User_Profile
    }

    user_create = requests.post(app_url + '/hms/user/create',json= create_user_dict, headers= headers, timeout=60)
    if user_create.status_code != 200:
        flash(f"Registration Failed{user_create.json().get('message')}","error")
        return redirect("/login")
    
    Doctor_ID = user_create.json().get('User_ID')

    #Adding doctor to department
    #Specialisation Lookup
    spec = {
        "Speciality": request.form.get("Speciality")
    }
    spec_lookup = requests.get(app_url + '/hms/departments/lookup',params = spec,headers=headers, timeout =60)
    departments = spec_lookup.json().get('department_details')[0]
    
    Dept_ID = departments["Dept_ID"]

    spec_dict = {
        "Doctor_ID": Doctor_ID,
        "Dept_ID" : Dept_ID,
        "Dept_Position": request.form.get("Dept_Position")

    }
    
    doc_assign = requests.post(app_url + '/hms/departments/assign',json = spec_dict, headers=headers,timeout = 60)
    if doc_assign.status_code != 200:
        flash("Doctor Assignment Failed","error")
        return redirect("/dashboard")
    
    flash("User Create Success","success")
    return render_template("register_success.html",user_token = sid ,User_ID = Doctor_ID,User_Type = 'ADMIN')

@app.route('/create_department', methods=['POST'])
@session_wrapper
def Create_Department(sid):
    if not sid:
        return redirect("/login")
    headers ={
         "Authorization": sid['token']
    }
   
    #Creating new department 

    dept_dict = {
        "Speciality" :request.form.get("Department_Name"),
        "Details": request.form.get("Department_Details",None)
    }

    dept_create = requests.post(app_url + '/hms/departments/create', json = dept_dict, 
    headers = headers, timeout = 60)
    if dept_create.status_code != 200:
        flash("Department Create Failed","error")
        return redirect("/doctor_register")
    
    flash("Department Create Successfully","success")
    return redirect("/doctor_register")

@app.route('/login', methods=['GET', 'POST'])
@session_wrapper
def login(sid):
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Verify Creds With Backend
        login_dict = {
            "User_ID": username,
            "Password": password
        }

        # Generate auth token from backend
        http_resp = requests.post(app_url + '/hms/id/generate/token', json=login_dict, timeout=60)
        if http_resp.status_code != 200:
            flash("Login Failed","error")
            return redirect("/login")
        
        # Extract Auth Token and Save in session
        auth_token_str = http_resp.json().get('token', None)
        if not auth_token_str:
            flash("Login Failed","error")
            return redirect("/login")
            
        auth_token = jwt.decode(auth_token_str, jwt_public_str, algorithms = ["RS256"])
       
        headers = {
            "Authorization": auth_token_str
        }

        # Call backend to fetch user details
        lookup_dict = {
            "User_ID": username
        }
        user_lookup = requests.get(app_url + '/hms/user/lookup', params= lookup_dict, timeout = 60,headers = headers)
        if user_lookup.status_code != 200:
            flash("Login Failed","error")
            return redirect("/login")
        
        user_details = (user_lookup.json().get('user_details'))[0] 
        First_Name = user_details['First_Name']
        Last_Name = user_details['Last_Name']

        # Create a session id
        session_id = str(uuid.uuid4())
        my_session_dict = {
            "token": auth_token_str,
            "auth_token": auth_token,
            "First_Name": First_Name,
            "Last_Name": Last_Name,
            "User_Type": auth_token['role'].lower()
        }
        # Maintain SID -> Token Map
        session_dict[session_id] = my_session_dict

        # Tell Flask my Session ID
        session['sid'] = session_id 

        # Redirect to dashboard

        return redirect("/dashboard")
        
    if sid:
        return redirect("/dashboard")
    
    return render_template('login.html')

@app.route('/treatment_detail', methods=['GET'])
@session_wrapper
def treatment_detail(sid):
    if not sid:
        return redirect("/login")
    
    param_json = request.args.to_dict()
    
    lookup_dict = {
        "Appointment_ID": param_json["Appointment_ID"]
    }

    if "Patient_ID" in param_json:
        lookup_dict["Patient_ID"] = param_json["Patient_ID"]

    headers = {
        "Authorization" : sid['token']
    }
    
    treatments_lookup = requests.get(app_url + '/hms/treatments/lookup', params = lookup_dict, timeout = 60, headers = headers)
    if treatments_lookup.status_code != 200:
        ret_json = treatments_lookup.json()
        flash(f"Treatment Lookup Failed {ret_json['message']}","error")
        return redirect("/dashboard")  
    
    treatment_details = treatments_lookup.json().get('treatment_details')
    
    return render_template('treatment_detail.html',treatment = treatment_details[0],
       user_token = sid)

@app.route('/doctor_search', methods=['GET'])
@session_wrapper
def Doctor_Search(sid):
    if not sid:
        return redirect("/login")
    
    headers = {
         "Authorization" : sid['token']
    }

    dept_doctor_lookup = requests.get(app_url + "/hms/departments/doctor-lookup", timeout = 60, headers = headers)
    if dept_doctor_lookup.status_code != 200:
        flash(f"Doctor Lookup Failed {dept_doctor_lookup.status_code}","error")
        return redirect("/dashboard")

    doctors_list = dept_doctor_lookup.json().get("doctordept_details")
    
    # Check for speciality in filter
    speciality = request.args.get("speciality", None)

    # Build Specialities list
    specialities = sorted({d["Specialities"] for d in doctors_list})

    doctors = []
    Details = None
    if speciality:
        doctors = [d for d in doctors_list
                   if d["Specialities"].lower() == speciality.lower()]
        Details = doctors[0]['Details']
        
  
    return render_template("doctor_search.html", \
        user_token  = sid, \
        specialities=specialities,
        selected_speciality= speciality,
        doctors=doctors, Details = Details) 

@app.route('/book_appointment', methods=['GET','POST'])
@session_wrapper
def Book_Appointment(sid):
    if not sid:
        return redirect("/login")
    
    headers = {
        "Authorization" : sid['token']
    }
    
    Doctor_ID = request.args.get("Doctor_ID")
    if not Doctor_ID:
        flash(f"Select the Doctor {Doctor_ID}", "error")
        return redirect("/dashboard")
    Slot = None
    Appointment_Date = request.args.get("date", None)

    if request.method == 'POST':
        Slot = request.form.get("slot", None)
        Appointment_Date = request.form.get("date", None)


    if request.method == 'GET' or \
        not Slot:        
        
        lookup_dict = {
            "User_ID" : Doctor_ID
        }

        dept_doctor_lookup = requests.get(app_url + "/hms/departments/doctor-lookup",params = lookup_dict,timeout = 60, headers = headers)
        if dept_doctor_lookup.status_code != 200:
            flash(f"Doctor Lookup Failed {dept_doctor_lookup.status_code}","error")
            return redirect("/dashboard")
        
        doctor = dept_doctor_lookup.json().get("doctordept_details")[0]
       
        # Get Slots
        date_list = get_next_7_days()
        if not Appointment_Date:
            Appointment_Date = date_list[0]
        slot_date = datetime.strptime(Appointment_Date, '%d %B %Y').strftime('%Y-%m-%d')
        slot_args = {
            "Doctor_ID" : Doctor_ID,
            "Appointment_Date" : slot_date
        }
        slots_lookup = requests.get(app_url + "/hms/slots/availability",params = slot_args,timeout = 60, headers = headers)
        if slots_lookup.status_code != 200:
                slot_reply = slots_lookup.json()
                flash(f"Slots Lookup Failed {slot_reply['message']}","error")
                return redirect("/dashboard")
        
        Available_Slots = slots_lookup.json().get('Free_Slots') 
        slot_list = []
        for f_slot in Free_Slots:
            slot_list.append({
                "slot": f_slot,
                "available": True if f_slot in Available_Slots else False
            })
      
        return render_template("book_appointment.html",user_token = sid, days = date_list, 
        selected_date = Appointment_Date, doctor= doctor, available = slot_list, User_Type = sid['auth_token']['role'])
    
    #Confirm Booking
    Patient_ID = request.form.get('patient_id', sid['auth_token']['user'])
    appt_details =  {
        "Appointment_Time": Slot,
        "Patient_ID": Patient_ID ,
        "Appointment_Date": datetime.strptime(Appointment_Date, '%d %B %Y').strftime('%Y-%m-%d'),
        "Doctor_ID": Doctor_ID
    }
    

    appt_create = requests.post(app_url + "/hms/appointment/create", json = appt_details, timeout =60 , headers = headers)
    if appt_create.status_code != 200:
        flash(f"Booking Failed {appt_details}","error")
        return redirect("/doctor_search")
    
    flash("Booking Confirmed","success")
    return redirect("/dashboard")

@app.route('/close_appointment', methods=['POST'])
@session_wrapper
def Close_Appointment(sid):
    if not sid:
        return redirect("/login")
    
    headers = {
        "Authorization": sid['token']
    }
    
    Appointment_ID = request.args.get("Appointment_ID")
    Save = request.args.get("Save",None)

    #Upload to database if Save is Y
    if Save:
        treatment = {
            "Appointment_ID": Appointment_ID,
            "Diagnosis": request.form.get('Diagnosis',None),
            "Prescription": request.form.get('Prescription',None),
            "Notes": request.form.get('Notes')
        }
        
        treatment_upload = requests.post(app_url + '/hms/treatments/upload',json = treatment,headers=headers, timeout = 60)
        if treatment_upload.status_code != 200:
            flash(f"Upload Failed{treatment_upload.json()['message']}","error")
            return redirect("/dashboard")
        
        appt_complete_dict = {
            "Appointment_ID": Appointment_ID,
            "Appointment_Status":'COMPLETED'
        }

        appointment = requests.put(app_url + '/hms/appointment/update',params=appt_complete_dict,headers=headers,timeout=60)
        if appointment.status_code != 200:
            flash(f"Complete Failed {appointment.json()['message']}","error")
            return redirect("/dashboard")
        
        flash("Uploaded Successfully","success")
        return redirect("/dashboard")
    
    #Lookup Appointments
    lookup_dict = {
        "Appointment_ID": Appointment_ID
     }

    appointments_lookup = requests.get(app_url + '/hms/appointments/lookup', params = lookup_dict, timeout = 60, headers = headers)
    if appointments_lookup.status_code != 200:
        flash("Appointment Lookup Failed","error")
        return redirect("/dashboard") 
        
    appointment = appointments_lookup.json().get('appointment_details')[0]
    Patient_ID = appointment['Patient_ID']

    #Patient Lookup
    lookup_dict = {
                "User_ID": Patient_ID
            }
            
    user_lookup = requests.get(app_url + '/hms/user/lookup', params= lookup_dict, timeout = 60,headers = headers)
    if user_lookup.status_code != 200:
        flash("User Lookup Failed","error")
        return redirect("/dashboard")
            
    user_details = (user_lookup.json().get('user_details'))[0]
    Age = calculate_age(user_details['Date_Of_Birth'])
    
    
    return render_template("treatment_upload.html",user_token=sid,
        Appointment_ID=Appointment_ID,
        Appointment_Date = appointment['Appointment_Date'],
        Appointment_Time = appointment['Appointment_Time'], Age = Age, 
        Sex = user_details['Sex'],First_Name = user_details['First_Name'], 
        Last_Name = user_details['Last_Name'])

@app.route('/cancel_appointment', methods=['POST'])
@session_wrapper
def Cancel_Appointment(sid):
    if not sid:
        return redirect("/login")
    
    headers = {
        "Authorization": sid['token']
    }
    
    Appointment_ID = request.args.get("Appointment_ID")
    Confirm = request.args.get("Confirm")
    Patient_ID = request.args.get("Patient_ID", sid['auth_token']['user'])

    if not Appointment_ID:
        flash("Appointment ID missing","error")
        return redirect("/dashboard")

    lookup_dict = {
        "Appointment_ID": Appointment_ID
    }
    
    if sid['auth_token']['role'] == 'DOCTOR':
        lookup_dict['Patient_ID'] = Patient_ID

    appointments_lookup = requests.get(app_url + '/hms/appointments/lookup', params = lookup_dict, timeout = 60, headers = headers)
    if appointments_lookup.status_code != 200:
        flash("Appointment Lookup Failed","error")
        return redirect("/dashboard") 
    print(appointments_lookup.json())
    appointment_details = appointments_lookup.json().get('appointment_details')[0]

    if not Confirm:
        return render_template("cancel_appointment.html", user_token = sid, appointment= appointment_details)

    #Delete in backend
    appt_cancel_dict = {
        "Appointment_ID": Appointment_ID ,
        "Appointment_Status": 'CANCELLED'
    }
   
    appt_cancel = requests.put(app_url + '/hms/appointment/update', params = appt_cancel_dict, headers = headers, timeout = 60)
    if appt_cancel.status_code != 200:
        flash("Appointment Cancel Failed","error")
    else:
        flash("Appointment Cancelled","success")
    return redirect("/dashboard")
        
@app.route('/delete_user', methods=['GET','POST'])
@session_wrapper
def Delete_User(sid):
    if not sid:
        return redirect("/login")
    
    headers = {
        "Authorization": sid['token']
    }
    
    
    User_ID = request.args.get("User_ID")
    user_dict = {
        "User_ID": User_ID
    }
    user_lookup = requests.get(app_url + '/hms/user/lookup', params = user_dict, headers = headers,
    timeout = 60)
    if user_lookup.status_code != 200:
        message = user_lookup.json().get("message")
        flash(f"User lookup: {message}","error")
        return redirect("/dashboard")
    user_details = user_lookup.json().get("user_details")[0]
    First_Name = user_details["First_Name"]
    Last_Name = user_details["Last_Name"]
    User_Type = user_details["User_Type"]

    if request.method == 'GET':
        return render_template("user_delete.html",user_token = sid, First_Name = First_Name,
            Last_Name = Last_Name, User_ID = User_ID)

    cancel_appt = request.form.get("cancel_appointments")
    if User_Type == 'DOCTOR':
        lookup_dict = {
            "Doctor_ID": User_ID,
            "Appointment_Status": 'SCHEDULED'
        }
    if User_Type == 'PATIENT':
        lookup_dict = {
            "Patient_ID": User_ID,
            "Appointment_Status": 'SCHEDULED'
        }
    
    appt_lookup = requests.get(app_url + '/hms/appointments/lookup',params = lookup_dict,
        headers = headers, timeout = 60)
    
    if cancel_appt != "on":
        #Appointment lookup
        if appt_lookup.status_code != 200:
                message = appt_lookup.json().get("message")
                flash(f"{message}","error")
                return redirect("/dashboard")
        
        appointment_details = appt_lookup.json().get("appointment_details")
        if len(appointment_details) > 0:
            flash("Cancel all upcoming appointments before delete","error")
            return redirect("/dashboard")
    else:
        # Now call Backend to cancel all the appointments for this User.
        appt_cancel_dict = {
            "Appointment_Status":'CANCELLED',
            f"{'Patient_ID' if User_Type == 'PATIENT' else 'Doctor_ID'}": User_ID
        }

        appointment = requests.put(app_url + '/hms/appointment/update',params=appt_cancel_dict,headers=headers,timeout=60)
        if appointment.status_code != 200:
            flash(f"Cancel Failed {appointment.json()['message']}","error")
            return redirect("/dashboard")
        
    #User Delete 
    delete_dict = {
        "User_ID": User_ID
    }
    user_del = requests.delete(app_url + '/hms/user/delete', params = delete_dict,
        headers = headers, timeout = 60 )
    
    if user_del.status_code != 200:
        message = user_del.json().get("message")
        flash(f"{message}","error")
        return redirect("/dashboard")
    
    user = user_del.json().get("User_ID")
    flash(f"User {user} deleted","success")
    return redirect("/dashboard")
    
@app.route('/dashboard', methods=['GET'])
@session_wrapper
def dashboard(sid):
    if not sid:
        return redirect("/login")
    
    headers = {
        "Authorization" : sid['token']
    } 

    if sid['auth_token']['role'] == 'PATIENT':
        #Upcoming Appointments
        lookup_dict = {
            "Patient_ID": sid['auth_token']['user']
        }

        appointments_lookup = requests.get(app_url + '/hms/appointments/lookup', params = lookup_dict, timeout = 60, headers = headers)
        if appointments_lookup.status_code != 200:
            flash("Appointment Lookup Failed","error")
            return redirect("/dashboard") 
        
        upcoming_appointments = appointments_lookup.json().get('appointment_details')

        #Treatment Info
        treatments_lookup = requests.get(app_url + '/hms/treatments/lookup', params = lookup_dict, timeout = 60, headers = headers)
        if treatments_lookup.status_code != 200:
            flash("Treatment Lookup Failed","error")
            return redirect("/dashboard") 
        
        treatment_details = treatments_lookup.json().get('treatment_details')
        
        return render_template('patient_dashboard.html', treatments = treatment_details, \
        user_token = sid, appointments = upcoming_appointments)
    
    if sid['auth_token']['role'] == 'DOCTOR':
        
        #Query all Appointments
        lookup_dict = {
            "Doctor_ID": sid['auth_token']['user'],
            "Appointment_Status": "ALL"
        }

        appointments_lookup = requests.get(app_url + '/hms/appointments/lookup', params = lookup_dict, timeout = 60, headers = headers)
        if appointments_lookup.status_code != 200:
            flash("Appointment Lookup Failed","error")
            return redirect("/dashboard") 
        
        all_appointments = appointments_lookup.json().get('appointment_details')
        
        # Filter only upcoming appointments
        upcoming_appointments = [ u_appt \
            for u_appt in all_appointments \
                if u_appt['Appointment_Status'] == "SCHEDULED"]

        # Lookup Unique Patients for this Doc
        pid_list = sorted({p["Patient_ID"] for p in all_appointments})
        patients = []
        for pid in pid_list:
            lookup_dict = {
                "User_ID": pid 
            }
            user_lookup = requests.get(app_url + '/hms/user/lookup', params= lookup_dict, timeout = 60,headers = headers)
            if user_lookup.status_code != 200:
                flash("User Lookup Failed","error")
                return redirect("/dashboard")
            
            if len(user_lookup.json().get('user_details',[])) != 1:
                continue

            user_details = user_lookup.json().get('user_details')[0]
            user_details['Age'] = calculate_age(user_details['Date_Of_Birth'])
            patients.append(user_details)
        #Get Doctor's Available Slots
        slot_dict = {
            "Doctor_ID": sid["auth_token"]['user']
        }
        slot_lookup = requests.get(app_url + '/hms/slots/lookup', params = slot_dict, headers= headers,timeout =60)
        if slot_lookup.status_code != 200:
            available_slots = {
                "Start_Date": date.today().strftime("%Y-%m-%d"),
                "End_Date": date.today().strftime("%Y-%m-%d"),
                "Days_Available":[]
            }
        else:    
            available_slots = slot_lookup.json().get('Slot')
            available_slots["Days_Available"] = sorted({d.lower() for d in available_slots['Days_Available']})
        
        # Get all Appointment Slots for the doctor
        return render_template('doctor_dashboard.html', user_token = sid,
            appointments=upcoming_appointments, patients=patients, 
            avail = available_slots)

    if sid['auth_token']['role'] == 'ADMIN':

        #Lookup to display Upcoming Appointments for the day
        

        appointments_lookup = requests.get(app_url + '/hms/appointments/lookup', timeout = 60, headers = headers)
        if appointments_lookup.status_code != 200:
            resp_json = appointments_lookup.json()
            flash("Appointment Lookup Failed","error")
            return f"Appointment Failed {resp_json['message']}"
        
        appointments = appointments_lookup.json().get('appointment_details')
        
        upcoming_appt = len(appointments)

        #Lookup to display All registered Doctors 
        
        doc_lookup = requests.get(app_url + "/hms/departments/doctor-lookup",timeout = 60, headers = headers)
        if doc_lookup.status_code != 200:
            flash("Doctor Lookup Failed","error")
            return "Doctor Lookup Failed"

        doctors = doc_lookup.json().get('doctordept_details')
        registered_doctors = len(doctors)

        #Lookup to display ALL registered Patients
        user_dict = {
            "User_Type": 'PATIENT',
            "User_Status": 'ACTIVE'
        }
        user_lookup = requests.get(app_url + '/hms/user/lookup', params = user_dict, headers=headers,timeout=60)
        if user_lookup.status_code != 200:
            flash("Patient Lookup Failed")
            return "Doctor Lookup Failed"
        
        patients = user_lookup.json().get('user_details')

        for patient in patients:
            patient['Age'] = calculate_age(patient['Date_Of_Birth'])
        
        registered_patients = len(patients)

        return render_template("/admin_dashboard.html", user_token = sid, appointments=appointments, 
            doctors = doctors, patients = patients, registered_doctors = registered_doctors,
            registered_patients = registered_patients, upcoming_appt = upcoming_appt)
    
@app.route("/edit-profile", methods=['GET', 'POST'])
@session_wrapper
def edit_profile(sid):
    if not sid:
        return redirect("/login")
    
    if request.method == 'GET':
        User_ID = request.args.get("User_ID", sid['auth_token']['user'])
    else:
        User_ID = request.form.get("User_ID", sid['auth_token']['user'])

    # Call backend to fetch user details
    lookup_dict = {
        "User_ID": User_ID
    }

    headers = {
            "Authorization": sid['token']
    }

    user_lookup = requests.get(app_url + '/hms/user/lookup', params= lookup_dict, timeout = 60,headers = headers)
    if user_lookup.status_code != 200:
        flash("User Lookup Failed","error")
        return redirect("/dashboard")
    
    user_details = (user_lookup.json().get('user_details'))[0]
    User_Type = user_details['User_Type']
    if request.method == 'GET':
        user_details['Sex'] = valid_gender_str[user_details['Sex']]
        return render_template('edit_profile.html', user=user_details, 
            user_token = sid, User_Type = User_Type)
    
    print(f"Handling Update {user_details['User_ID']}")
    #Handling Update
    user_update_dict = {
        "User_ID": user_details["User_ID"]
    }
    if sid['auth_token']['role'] == 'DOCTOR':
        User_Profile = {
            "Qualifications": request.form.get("Qualification"),
            "Experience": request.form.get("Experience"),
            "Expertise": request.form.get("Expertise"),
            "Bio": request.form.get("Bio")
        }
        user_update_dict["User_Profile"] = User_Profile

    First_Name = request.form.get('First_Name')
    Last_Name = request.form.get('Last_Name')
    Phone_Number = request.form.get('Phone_Number')
    Email_ID = request.form.get('Email_ID')
    Sex = request.form.get('Sex')[0].upper()
    Address = request.form.get('Address')
    Date_Of_Birth = request.form.get('Date_Of_Birth')
    Current_Password = request.form.get('cur_password')
    New_Password = request.form.get('new_password')

    if First_Name.lower() != user_details['First_Name']:
        user_update_dict["First_Name"] = First_Name
    
    if Last_Name.lower() != user_details['Last_Name']:
        user_update_dict["Last_Name"] = Last_Name 
    
    if Address != user_details['Address']:
        user_update_dict["Address"] = Address

    if Phone_Number != user_details['Phone_Number']:
        user_update_dict["Phone_Number"] = Phone_Number 
    
    if Email_ID != user_details['Email_ID']:
        user_update_dict["Email_ID"] = Email_ID 
    
    if Sex != user_details['Sex']:
        user_update_dict["Sex"] = Sex

    if Date_Of_Birth != user_details['Date_Of_Birth']:
        user_update_dict["Date_Of_Birth"] = Date_Of_Birth 
   
    headers = {
        'Authorization': sid['token'] 
    }
    print(json.dumps(user_update_dict))
    if New_Password:
        #Verifying Current_Password with backend
        req_json = {
            "User_ID": user_details["User_ID"],
            "Password": Current_Password
        }
        http_resp = requests.post(app_url + '/hms/user/check-password', json = req_json, headers = headers, timeout = 60)
        if http_resp.status_code != 200:
            flash("Invalid Password","error")
            return redirect("/dashboard")

        user_update_dict["Password"] = New_Password

    if len(user_update_dict.keys()) > 1:
        # Update the user record
        http_resp = requests.post(app_url + '/hms/user/update', json = user_update_dict, headers = headers, timeout = 60)
        resp_json = http_resp.json()
        if http_resp.status_code != 200:
            flash(f"Error Updating Profile: {resp_json['message']}","error")
            return redirect("/dashboard")
        else:
            flash("Profile updated successfully","success")
    else:
        flash("No Updates Given", "warning")
        return render_template("edit_profile.html", user_token = sid ,user=user_details, User_Type=sid['auth_token']['role'])
    
    if User_ID == sid['auth_token']['user']:
        sid['First_Name'] = user_update_dict.get('First_Name', user_details['First_Name'])
        sid['Last_Name'] = user_update_dict.get('Last_Name', user_details['Last_Name'])

    return redirect("/dashboard")

@app.route("/patient_history")
@session_wrapper
def Patient_History(sid):
    if not sid:
        return redirect("/login")
    
    headers = {
        "Authorization" : sid['token']
    } 

    Patient_ID = request.args.get('Patient_ID')

    lookup_dict = {
        "Patient_ID": Patient_ID
    }

    #Treatment Info
    treatments_lookup = requests.get(app_url + '/hms/treatments/lookup', params = lookup_dict, timeout = 60, headers = headers)
    if treatments_lookup.status_code != 200:
        flash("Treatment Lookup Failed","error")
        return redirect("/dashboard") 
        
    treatment_details = treatments_lookup.json().get('treatment_details')
    return render_template("patient_history.html",user_token = sid,treatments=treatment_details)

@app.route("/logout")
@session_wrapper
def logout(sid):
    sid = session.get("sid", None)
    if sid:
        session_dict.pop(sid,None)
        session.clear()
    return redirect("/login")

@app.route('/doctor_profile', methods=['GET'])
@session_wrapper
def Doctor_Profile(sid):
    if not sid:
        return redirect("/login")
    
    headers = {
        "Authorization": sid['token']
    }

    Doctor_ID = request.args.get('User_ID')

    lookup_dict = {
            "User_ID" : Doctor_ID
    }
    
    # Do DoctorLookup
    dept_doctor_lookup = requests.get(app_url + "/hms/departments/doctor-lookup",params = lookup_dict,timeout = 60, headers = headers)
    if dept_doctor_lookup.status_code != 200:
        flash(f"Doctor Lookup Failed {dept_doctor_lookup.status_code}","error")
        return redirect("/dashboard")
        
    doctor = dept_doctor_lookup.json().get("doctordept_details")[0]
    User_Profile = json.loads(doctor["User_Profile"])

    return render_template("doctor_profile.html", user_token = sid,doctor=doctor,User_Profile = User_Profile)

@app.route('/patient_profile', methods=['GET'])
@session_wrapper
def Patient_Profile(sid):
    if not sid:
        return redirect("/login")
    
    headers = {
        "Authorization": sid['token']
    }

    Patient_ID = request.args.get('User_ID')

    lookup_dict = {
            "User_ID" : Patient_ID
    }
    
    # Do DoctorLookup
    user_lookup = requests.get(app_url + "/hms/user/lookup",params = lookup_dict,timeout = 60, headers = headers)
    if user_lookup.status_code != 200:
        flash(f"Patient Lookup Failed","error")
        return redirect("/dashboard")
        
    patient = user_lookup.json().get("user_details")[0]
    Age = calculate_age(patient['Date_Of_Birth'])
    patient["Age"] = Age


    return render_template("patient_profile.html", user_token = sid,patient=patient)

@app.route('/update_availability', methods=['POST'])
@session_wrapper
def Update_Availability(sid):
    if not sid:
        return redirect("/login")
    
    headers = {
        "Authorization" : sid['token']
    }

    #Post In Database
    Days_Available = request.form.getlist("Days_Available")
    Days_Available = sorted({d.upper() for d in Days_Available})
    slot_dict = {
    "Doctor_ID" : sid['auth_token']['user'],
    "Start_Date": request.form.get('Start_Date'),
    "End_Date": request.form.get('End_Date'),
    "Days_Available": Days_Available 
    }

    updated_slots = requests.post(app_url + '/hms/slots/create', json = slot_dict,headers=headers,timeout = 60)
    if updated_slots.status_code != 200:
        flash(f"Update Failed {updated_slots.json().get('message')}","error")
        return redirect("/dashboard")

    flash("Update Successful","success")
    return redirect("/dashboard")

@app.route('/cancel_all_appt', methods=['POST'])
@session_wrapper
def Cancel_All_Appointments(sid):
    if not sid:
        return redirect("/login")
    headers ={
         "Authorization": sid['token']
    }

    User_Type = sid['auth_token']['role']
    User_ID = sid['auth_token']['user']
    appt_cancel_dict = {
         "Appointment_Status":'CANCELLED',
        f"{'Patient_ID' if User_Type == 'PATIENT' else 'Doctor_ID'}": User_ID
    }

    appointment = requests.put(app_url + '/hms/appointment/update',params=appt_cancel_dict,headers=headers,timeout=60)
    if appointment.status_code != 200:
        flash(f"Cancel Failed {appointment.json()['message']}","error")
        return redirect("/dashboard")

    flash("Cancelled All Appointments","success")
    return redirect("/dashboard")

@app.route('/user-search', methods=['GET', 'POST'])
@session_wrapper
def User_Search(sid):
    if not sid:
        return redirect("/login")
    headers ={
         "Authorization": sid['token']
    }

    if request.method == 'GET':
        return render_template("user_search.html",user_token = sid)
    
    lookup_dict = {}
    parameters = request.form.to_dict()
    for key in ["First_Name","Last_Name","Phone_Number","User_Type"]:
        if key in parameters:
            lookup_dict[key] = parameters[key]
    print(parameters)
    
    user_lookup = requests.get(app_url + '/hms/user/lookup',params = lookup_dict,
        headers = headers, timeout = 60)
    
    if user_lookup.status_code != 200:
        flash("Search Failed","error")
        return redirect("/dashboard")
    
    users = user_lookup.json().get("user_details")
    flash("Search Successful","success")

    return render_template("user_search.html", user_token = sid, users = users)


@app.route('/', methods=['GET'])
@session_wrapper
def home(sid):
     
     if not sid:
        return redirect("/login")
     else:
         return redirect("/dashboard") 
    
if __name__ == '__main__' :
    # Read the config from config.json
    config_dict = json.loads(open("fe_config.json",'r').read())
    
    # Set My Templates Dir
    app.jinja_loader = FileSystemLoader(config_dict["template_dir"])
    app_url = config_dict["app_url"]
    
    #Load JWT Private and Public Keys
    jwt_public_str = open(config_dict["jwt_public"]).read()

    # Get our auth token
    my_auth_token = gen_backend_token(config_dict['account_id'], config_dict['account_pwd'])
    app.secret_key = "a-very-secret-key"
    app.run(debug=True, port=9001)
