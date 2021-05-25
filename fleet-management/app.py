

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from sendemail import sendmail,sendgridmail
import smtplib

  
app = Flask(__name__)
  
app.secret_key = 'a'

  
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'ECPmhrTKNs'
app.config['MYSQL_PASSWORD'] = 'aBj66D5O5U'
app.config['MYSQL_DB'] = 'ECPmhrTKNs'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('demo.html')



@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' :
        batch = request.form['batch']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username = % s', (username, ))
        account = cursor.fetchone()
        print(account)
        if account:
            msg = 'user data already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, %s, % s, % s, % s)',(batch, username, email, password))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            TEXT = "Hello "+username + ",\n\n"+ """Thanks for registring at fleet management portal """ 
            message  = 'Subject: {}\n\n{}'.format("smartinterns Carrers", TEXT)
            #sendmail(TEXT,email)
            #sendgridmail(email,TEXT)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)



@app.route('/dashboard')
def dash():
    
    return render_template('dashboard.html')



@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
   
  
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username = % s AND password = % s', (username, password ),)
        account = cursor.fetchone()
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            userid=  account[0]
            session['username'] = account[1]
            msg = 'Logged in successfully !'
            
            msg = 'Logged in successfully !'
            return render_template('dashboard.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

    

@app.route('/apply',methods =['GET', 'POST'])
def apply():
     msg = ''
     if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        destination= request.form['destination']
        date = request.form['date']
        time = request.form['time']
        jobs = request.form['s']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM job WHERE userid = % s', (session['id'], ))
        account = cursor.fetchone()
        print(account)
        if account:
            msg = 'your trip details have been updated!'
            return render_template('apply.html', msg = msg)

               
         
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO job VALUES (% s, % s, % s, % s, % s, % s, % s)', (session['id'],username, email, destination, date, time, jobs))
        mysql.connection.commit() 
        msg = 'You have successfully updated!'
        session['loggedin'] = True
        TEXT = "Hello user,the current position has been " +jobs+"is requested"
         
       
        #sendgridmail("prawinta.sankar@gmail.com",TEXT)
         
         
         
     elif request.method == 'POST':
         msg = 'Please fill out the form !'
     return render_template('apply.html', msg = msg)




@app.route('/display')
def display():
    print(session["username"],session['id'])
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM job WHERE userid = % s', (session['id'],))
    account = cursor.fetchone()
    print("accountdislay",account)
 
    return render_template('display.html',account = account)




@app.route('/logout')

def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return render_template('home.html')

#@app.route('/admin')

#def admin():
    
    
#if __name__ == '__main__':
#   app.run(host='0.0.0.0',debug = True,port = 3000)
   
   
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug = True,port = 5000)