from flask import Flask
from flask import request
from flask import render_template
from flask import redirect, url_for, session
from secrets import get_secret_flask_session
from functools import wraps
import db
import secrets

app = Flask(__name__)
# app.secret_key = b'gdfgdrggfg1453'
app.secret_key = get_secret_flask_session()


def check_admin():
    return 'username' in session and 'username' == 'admin'


def current_user():
    return 'username' in session


def requires_admin(view):
    @wraps(view)
    def decorated(**kwargs):
        if not check_admin():
            return redirect('/login')
        return redirect('/login')
    return decorated


def req_current_user(view):
    @wraps(view)
    def decorated(**kwargs):
        if not current_user():
           return redirect('/login')
        view(**kwargs)
    return decorated 


@app.route('/', methods=["GET", "POST"])
def home():        
    return "Welcome to the Image Gallery User Database. For database admin functions please navigate to elisamek.codes/admin"


@app.route('/invalidLogin')
def invalidLogin():
    return "Invalid login"


@app.route('/validLogin')
def validLogin():
    return "Valid login"

@app.route('/inc')
def inc():
    if 'value' not in session:
        session['value'] = 0
    session['value'] = session['value'] + 1
    return "<h1>"+str(session['value'])+"</h1>"


@app.route('/login', methods=['GET', 'POST'])
def login():
    db.connect()
    if request.method == 'POST':
        password = db.select_password(request.form["username"])
       
        form_pass = request.form["password"]
        if password != form_pass:
            return redirect('/login')
            
        else:
            session['username'] = request.form["username"]
            return redirect('/validLogin')
    else:
        db.close()
        return render_template('login.html')


@app.route('/debugSession')
def debugSession():
    result = " "
    for key,value in session.items():
        result += key+"->"+str(value)+"<br />"
    return result

@req_current_user
@requires_admin
@app.route('/admin', methods=["GET", "POST"])
def index():
    db.connect()
    return render_template('index.html', username=db.select_all_usernames("users"))


@requires_admin
@app.route('/admin/edit/<username>')
def edit(username):
     return render_template('edit.html', username=username)


@app.route('/admin/edit/modify', methods=['POST'])
def modify():
    db.connect()
    username = request.form['username']
    password = request.form['password']
    full_name = request.form['full_name']
    db.edit_user(username, password, full_name)
    res = db.select_user_info(username, 'users') 
    db.close()
    return render_template('modify.html', user_info=res)

@req_current_user
@requires_admin    
@app.route('/admin/addUser')
def addUser():
    return render_template('addUser.html')

@req_current_user
@requires_admin
@app.route('/admin/addUser/added', methods=['POST'])
def added():
    db.connect()
    username = request.form['username']
    password = request.form['password']
    full_name = request.form['full_name']
    db.add_user(username, password, full_name)
    res = db.select_user_info(username, 'users') 
    db.close()
    return render_template('added.html', user_info=res)

@requires_admin
@app.route('/admin/edit/delete', methods=['POST'])
def delete():
    db.connect()
    username = request.form['username']    
    username = username.strip()
    db.delete_user(username)
    db.close()    
    return render_template('deleteSuccessful.html',username= username)

@req_current_user
@requires_admin
@app.route('/admin/delete', methods=['POST'])
def main_delete():
    db.connect()
    username = request.form['username']    
    username = username.strip()
    db.delete_user(username)
    return render_template('deleteSuccessful.html',username= username)



