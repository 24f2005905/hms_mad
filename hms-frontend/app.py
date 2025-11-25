import json
from flask import Flask, render_template, request, redirect, url_for
from jinja2 import FileSystemLoader
import requests
import uuid
import jwt
import json
from flask import session
from functools import wraps

app = Flask(__name__)
app_url = None
session_dict = {}

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
            return "Invalid credentials", 401
        
        # Extract Auth Token and Save in session
        auth_token_str = http_resp.json().get('token', None)
        if not auth_token_str:
            return "Invalid credentials", 401
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
            return "Invalid Lookup", 401 
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
    
    return render_template('dashboard.html',first_name= sid['First_Name'], last_name= sid['Last_Name'])

@app.route('/', methods=['GET'])
@session_wrapper
def home(sid):
     
     if sid:
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
