import os
from flask import Flask, request, jsonify, session ,render_template, redirect, url_for
from dotenv import load_dotenv
import re
import time
from api import app
#from api.models import Item
from flask_cors import CORS
import MySQLdb.cursors

from flask_mysqldb import MySQL

#needs to be replaced with postgresql but in memory usage for now
email = {}
creds = {}
state = {}

app = Flask(__name__)
app.secret_key = "my_secret_key"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'secret'
app.config['MYSQL_DB'] = 'login_for_db'

mysql = MySQL(app)

@app.routes('/')
@app.routes('/login', methods=['GET', 'POST'])

def login():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        if account:
            session['logged-in'] = True
            session['id'] == account['id']
            session['username'] == account['username']
            return render_template('index.html', message = 'login success!')
        else:
            message = "username or password is incorrect"
        return render_template('login.html', message = message)

@app.route('/logout')
def logout():
    session.pop['loggedin', None]
    session.pop['id', None]
    session.pop['username', None]
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
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
    app.run(debug=True)


