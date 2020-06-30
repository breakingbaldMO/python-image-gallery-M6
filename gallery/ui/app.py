from flask import Flask
from flask import request
from flask import render_template
from flask import redirect, url_for
from . import db
from . import secrets


app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def home():
    
        
    return "Welcome to the Image Gallery User Database. For database admin functions please navigate to elisamek.codes/admin"


@app.route('/admin', methods=["GET", "POST"])
def index():
    db.connect()
        
    return render_template('index.html', username=db.select_all_usernames("users"))

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
    
@app.route('/admin/addUser')
def addUser():
    return render_template('addUser.html')

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

@app.route('/admin/edit/delete', methods=['POST'])
def delete():
    db.connect()
    username = request.form['username']    
    username = username.strip()
    db.delete_user(username)
    db.close()    
    return render_template('deleteSuccessful.html',username= username)

@app.route('/admin/delete', methods=['POST'])
def main_delete():
    db.connect()
    username = request.form['username']    
    username = username.strip()
    db.delete_user(username)
    return render_template('deleteSuccessful.html',username= username)
