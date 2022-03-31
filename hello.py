from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)
import sys
from config import *
import os
import boto3
from pymysql import connections

app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}
table = 'user'


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

query = "SELECT id, username, password from user"
cursor = db_conn.cursor()

cursor.execute(query)
records = cursor.fetchall()

users = []

for row in records:
    users.append(User(id=row[0], username=row[1], password=row[2]))

#users.append(User(id=1, username='Anthony', password='password'))
#users.append(User(id=2, username='Becca', password='secret'))
#users.append(User(id=3, username='Carlos', password='somethingsimple'))


app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user

    #g.user = None

    #if 'username' in session:
    #    g.user = session['username']
        

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        user = 0
        
        for x in users:
            try:
                if x.username == username:
                    user = [x][0]
            except:
                error = 'Invalid username or password. Please try again!'
                return render_template('login-page.html', error = error)
                

        # user = [x for x in users if x.username == username][0]

        if user and user.password == password:
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('profile'))

        if user and user.password != password:
            error = 'Invalid username or password. Please try again!'
            return render_template('login-page.html', error = error)

        error = 'Invalid username or password. Please try again!'
        return render_template('login-page.html', error = error)

    return render_template('login-page.html')

@app.route('/AddEmp')
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('AddEmp.html',user=session['username'])

"""

@app.route('/protected')
def protected():
    if g.user:
        return render_template('protected.html',user=session['username'])
    return redirect(url_for('index'))

"""

@app.route('/dropsession')
def dropsession():
    session.pop('username', None)
    session.pop('user_id', None)
    g.user = None
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

"""
if __name__ == "__main__":
    app.run(debug=True)
"""
