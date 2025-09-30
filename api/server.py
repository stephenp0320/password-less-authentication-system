from os import environ as env
from flask import Flask, request, jsonify, session ,render_template, redirect, url_for
from dotenv import load_dotenv, find_dotenv
import re
import time
#from api import app
#from api.models import Item
#from flask_cors import CORS
import MySQLdb.cursors
from authlib.integrations.flask_oauth2 import ResourceProtector
from .validator import Auth0JWTBearerTokenValidator

require_auth = ResourceProtector()
validator = Auth0JWTBearerTokenValidator(
    "dev-8j5h1ji5u1tosodd.us.auth0.com",
    "{https://passwordless-auth-api.local}"
) 
require_auth.register_token_validator(validator)

from flask_mysqldb import MySQL

#needs to be replaced with postgresql but in memory usage for now
email = {}
creds = {}
state = {}

APP = Flask(__name__)
APP.secret_key = "my_secret_key"

APP.config['MYSQL_HOST'] = 'localhost'
APP.config['MYSQL_USER'] = 'root'
APP.config['MYSQL_PASSWORD'] = 'secret'
APP.config['MYSQL_DB'] = 'login_for_db'

mysql = MySQL(APP)

# <--- VALIDATOR CODE AUTHO --->

@APP.route('/api/public') # public endpoint that doesnt need authentication
def public():
    """no access token required"""
    return jsonify({"message": "Hello from public enpoint, no need for authentication to see this! "})

@require_auth()
@APP.route('/api/private') #private endpoint that needs a valid access token JWT
def private():
    """valid access token is required."""
    
    return jsonify({"message": "Hello from private endpoint, you need authentication to see this "})


@APP.route('/api/private-scoped')
@require_auth("read:messages")
def private_scoped():
    """valid access token and scope are needed"""
    return jsonify({"message": "Hello from a private endpoint! You need to be authenticated and have a scope of read:messages to see this."})
    












# <--- code for login and registration --->

@APP.route('/')
@APP.route('/login', methods=['GET', 'POST'])

def login():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return render_template('index.html', message = 'login success!')
        else:
            message = "username or password is incorrect"
        return render_template('login.html', message = message)
    return render_template('login.html', message=message)

@APP.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@APP.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            message = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            message = 'Username must contain only letters and numbers!'
        elif not username or not password or not email:
            message = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email))
            mysql.connection.commit()
            message = 'You have successfully registered!'
    return render_template('register.html', message=message)

if __name__ == "__main__":
    APP.run(debug=True)


