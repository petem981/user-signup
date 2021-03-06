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



@app.route('/', methods=['POST', 'GET'])
def validate_form():

    username = request.form['username']
    password = request.form['password']
    verify = request.form['verify']
    email = request.form['email']

    username_error = ''
    password_error = ''
    verify_error = ''
    email_error = ''

    if not 3 <= len(username) <= 20:
        username_error = 'Not a valid username, must be between 3-20 characters'
        username = ''
    if not 3 <= len(password) <= 20:
        password_error = 'Not a valid password, must be between 3-20 characters'
        password = ''
    if len(email) <= 1:
        email_error= ''
    if verify != password:
        verify_error = "Oopsies! Your passwords don't match"
        verify = ''
    if " " in username:
        username_error = 'Not a valid username, cannot contain spaces'
        username = ''
    if " " in password:
        password_error = 'Not a valid password, cannot contain spaces'
        password = ''
    if len(email) >= 1:
        if " " in email:
            email_error = 'Not a valid email, cannot contain spaces'
            email = ''
        if "@" not in email:
            email_error = 'Not a valid email'
            email = ''
        if "." not in email:
            email_error = 'Not a valid email'
            email = ''
    

    if not username_error and not password_error and not verify_error and not email_error:
        return redirect('/valid-form?username='+username)
    else:
        template = jinja_env.get_template('index.html')
        return template.render(username_error=username_error, password_error=password_error, verify_error=verify_error, email_error=email_error, username=username, password=password, verify=verify, email=email)

@app.route('/valid-form', methods=['POST', 'GET'])
def valid_form():
    username = request.args.get('username')
    template = jinja_env.get_template('welcome.html')
    return template.render(username=username)

app.run()