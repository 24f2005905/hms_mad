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

Free_Slots = ["09:00", "09:15", "09:30", "09:45",
        "10:00", "10:15", "10:30", "10:45",
        "11:00", "11:15", "11:30", "11:45", 
        "14:00", "14:15", "14:30", "14:45", 
        "15:00", "15:15", "15:30", "15:45",
        "16:00", "16:15", "16:30", "16:45"]

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

    headers = {
        "Authorization" : sid['token']
    }
    
    treatments_lookup = requests.get(app_url + '/hms/treatments/lookup', params = lookup_dict, timeout = 60, headers = headers)
    if treatments_lookup.status_code != 200:
        flash(f"Treatment Lookup Failed {treatments_lookup.status_code}","error")
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
    if speciality:
        doctors = [d for d in doctors_list
                   if d["Specialities"].lower() == speciality.lower()]
  
    return render_template("doctor_search.html", \
        user_token  = sid, \
        specialities=specialities,
        selected_speciality= speciality,
        doctors=doctors) 

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
      
        return render_template("book_appointment.html",user_token = sid, days = date_list, selected_date = Appointment_Date, doctor= doctor, available = slot_list)
    
    #Confirm Booking
    appt_details =  {
        "Appointment_Time": Slot,
        "Patient_ID":  sid['auth_token']['user'],
        "Appointment_Date": datetime.strptime(Appointment_Date, '%d %B %Y').strftime('%Y-%m-%d'),
        "Doctor_ID": Doctor_ID
    }
    

    appt_create = requests.post(app_url + "/hms/appointment/create", json = appt_details, timeout =60 , headers = headers)
    if appt_create.status_code != 200:
        flash(f"Booking Failed {appt_details}","error")
        return redirect("/doctor_search")
    
    flash("Booking Confirmed","success")
    return redirect("/dashboard")

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

    if not Appointment_ID:
        flash("Appointment ID missing","error")
        return redirect("/dashboard")

    lookup_dict = {
        "Patient_ID": sid['auth_token']['user'],
        "Appointment_ID": Appointment_ID
    }

    appointments_lookup = requests.get(app_url + '/hms/appointments/lookup', params = lookup_dict, timeout = 60, headers = headers)
    if appointments_lookup.status_code != 200:
        flash("Appointment Lookup Failed","error")
        return redirect("/dashboard") 
    
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
        

@app.route('/dashboard', methods=['GET'])
@session_wrapper
def dashboard(sid):
    if not sid:
        return redirect("/login")
    
    headers = {
        "Authorization" : sid['token']
    } 

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
    
    
    return render_template('dashboard.html', treatments = treatment_details, \
       user_token = sid, appointments = upcoming_appointments)

@app.route("/edit-profile", methods=['GET', 'POST'])
@session_wrapper
def edit_profile(sid):
    if not sid:
        return redirect("/login")
    
    # Call backend to fetch user details
    lookup_dict = {
        "User_ID": sid['auth_token']['user']
    }

    headers = {
            "Authorization": sid['token']
    }

    user_lookup = requests.get(app_url + '/hms/user/lookup', params= lookup_dict, timeout = 60,headers = headers)
    if user_lookup.status_code != 200:
        flash("User Lookup Failed","error")
        return redirect("/edit-profile")
    
    user_details = (user_lookup.json().get('user_details'))[0]

    if request.method == 'GET':
        user_details['Sex'] = valid_gender_str[user_details['Sex']]
        return render_template('edit_profile.html', user=user_details, 
            user_token = sid)
    
    #Handling Update
    user_update_dict = {
        "User_ID": user_details["User_ID"]
    }
    
    First_Name = request.form.get('First_Name')
    Last_Name = request.form.get('Last_Name')
    Phone_Number = request.form.get('Phone_Number')
    Email_ID = request.form.get('Email_ID')
    Sex = request.form.get('Sex')[0].upper()
    Current_Password = request.form.get('cur_password')
    New_Password = request.form.get('new_password')

    if First_Name.lower() != user_details['First_Name']:
        user_update_dict["First_Name"] = First_Name
    
    if Last_Name.lower() != user_details['Last_Name']:
        user_update_dict["Last_Name"] = Last_Name 

    if Phone_Number != user_details['Phone_Number']:
        user_update_dict["Phone_Number"] = Phone_Number 
    
    if Email_ID != user_details['Email_ID']:
        user_update_dict["Email_ID"] = Email_ID 
    
    if Sex != user_details['Sex']:
        user_update_dict["Sex"] = Sex 
    
    headers = {
        'Authorization': sid['token'] 
    }
    
    if New_Password:
        #Verifying Current_Password with backend
        req_json = {
            "User_ID": user_details["User_ID"],
            "Password": Current_Password
        }
        http_resp = requests.post(app_url + '/hms/user/check-password', json = req_json, headers = headers, timeout = 60)
        if http_resp.status_code != 200:
            flash("Invalid Password","error")
            return render_template("edit_profile.html", 
                user_token = sid,
                user=user_details)

        user_update_dict["Password"] = New_Password

    if len(user_update_dict.keys()) > 1:
        # Update the user record
        http_resp = requests.post(app_url + '/hms/user/update', json = user_update_dict, headers = headers, timeout = 60)
        if http_resp.status_code != 200:
            resp_json = http_resp.json()
            flash(f"Error Updating Profile: {resp_json['message']}","error")
            return render_template("edit_profile.html", user_token = sid, user=user_details)
        else:
            flash("Profile updated successfully","success")
    else:
        flash("No Updates Given", "warning")
        return render_template("edit_profile.html", user_token = sid ,user=user_details)
    return redirect("/dashboard")

@app.route("/history")
@session_wrapper
def history(sid):
    if not sid:
        return redirect("/login")
    else:
        return redirect("/dashboard") 

@app.route("/logout")
@session_wrapper
def logout(sid):
    sid = session.get("sid", None)
    if sid:
        session_dict.pop(sid,None)
        session.clear()
    return redirect("/login")

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
    app.secret_key = "a-very-secret-key"
    app.run(debug=True, port=9001)
