from flask import Flask, request, redirect
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    template = jinja_env.get_template('index.html')
    return template.render()

def verification(text):
    try:
        str(text)
        return True
    except ValueError:
        return False

@app.route('/user-signup', methods=['POST'])
def user_signup():
    signup = ''
    signup = signup.format(username='', password='', password_error='', verify='', verify_error='', email='', email_error='')
    return redirect('/validate-signup-form')

@app.route('/validate-signup-form', methods=['POST', 'GET'])
def validate_form():

    username = request.args.get('username')
    password = request.args.get('password')
    verify = request.args.get('verify')
    email = request.args.get('email')

    username_error = ''
    password_error = ''
    verify_error = ''
    email_error = ''

    if not verification(username):
        username_error = 'Not a Valid username'
        username = ''
    else:
        username = str(username)
        username = ''
    
    if not verification(password):
        password_error = 'Password must be longer than three characters and cannot contain spaces'
        password = '   '
    else:
        if password == verify:
            password = ''

    if not verification(verify):
        verify_error = 'Passwords do not match'
        verify = ''
    else:
        password = ''
        if verify == password:
            verify = ''

    if not verification(email):
        email_error = 'Not a Valid email'
        email = ''
    else:
        email = str(email)
        email = ''

    if not username_error and not password_error and not verify_error and not email_error:
        return redirect('/valid-form')
    else:
        return user_signup(username_error=username_error,
            password_error=password_error, verify_error=verify_error, 
            email_error=email_error,
            username=username,
            password=password,
            verify=verify,
            email=email)

@app.route('/valid-form', methods=['POST', 'GET'])
def valid_form():
    form = ''
    return "<h1>WooHoo! You're all signed up!</h1>"

app.run()