import json
from flask import Flask, render_template, request, redirect, url_for
from jinja2 import FileSystemLoader
import requests
import uuid
import jwt
import json
from flask import session, flash
from functools import wraps

app = Flask(__name__)
app_url = None
session_dict = {}
valid_gender_str = {
	'M': 'Male',
	'F': 'Female'
}

def session_wrapper(f):
    """ Session Wrapper Decorator"""
    @wraps(f)
    def sid_wrapper(*args, **kwargs):
        # Check for valid session
        sid = session.get('sid')
        kwargs['sid'] = session_dict.get(sid, None)
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
            "Last_Name": Last_Name
        }
        session_dict[session_id] = my_session_dict
        session['sid'] = session_id 

        # Redirect to dashboard

        return redirect("/dashboard")
        
    if sid:
        return redirect("/dashboard")
    
    return render_template('login.html')

@app.route('/dashboard', methods=['GET'])
@session_wrapper
def dashboard(sid):
    if not sid:
        return redirect("/login")
    
    return render_template('dashboard.html',First_Name= sid['First_Name'], Last_Name= sid['Last_Name'])

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
        return "Invalid Lookup", 401 
    user_details = (user_lookup.json().get('user_details'))[0]

    if request.method == 'GET':
        user_details['Sex'] = valid_gender_str[user_details['Sex']]
        return render_template('edit_profile.html', user=user_details)
    
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
            return render_template("edit_profile.html", user=user_details)

        user_update_dict["Password"] = New_Password

    if len(user_update_dict.keys()) > 1:
        # Update the user record
        http_resp = requests.post(app_url + '/hms/user/update', json = user_update_dict, headers = headers, timeout = 60)
        if http_resp.status_code != 200:
            resp_json = http_resp.json()
            flash(f"Error Updating Profile: {resp_json['message']}","error")
            return render_template("edit_profile.html", user=user_details)
        else:
            flash("Profile updated successfully","success")
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
