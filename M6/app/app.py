from flask import Flask
from flask import request
from flask import render_template
from flask import redirect, url_for, session
import s3
import db
import base64

app = Flask(__name__)

app.secret_key = b'gdfgdrggfg1453'


def check_admin():
    return 'admin' in session


def current_user():
    return 'username' in session


@app.route('/', methods=["GET", "POST"])
def home():
    if not current_user():
        return redirect('/login')
    return render_template("main.html")


@app.route('/upload', methods=["POST", "GET"])
def upload():
    return render_template('upload.html')


@app.route('/gallery', methods=["POST", "GET"])
def gallery():
    images = []
    user = session.get('username')
    image_names = db.select_all_images(user)
    for name in image_names:
        image_data = s3.get_object("eli.samek.image-gallery", name[0])["Body"].read()
        image = base64.b64encode(image_data).decode("utf-8")
        images.append(image)
    return render_template('gallery.html', images=images)


@app.route('/uploadImage', methods=["POST", "GET"])
def uploadImage():
    if request.method == "POST":
        f = request.files['file']
        user = session.get('username')
        filename = {f.filename}
        key = user + "-" + str({f.filename})
        s3.put_object("eli.samek.image-gallery", key, f)
        db.add_image(user, key)
        return render_template('main.html')


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
            return redirect('/')
    else:
        db.close()
        return render_template('login.html')


@app.route('/debugSession')
def debugSession():
    result = " "
    for key, value in session.items():
        result += key + "->" + str(value) + "<br />"
    return result


@app.route('/inc')
def inc():
    if 'value' not in session:
        session['value'] = 0
    session['value'] = session['value'] + 1
    return "<h1>" + str(session['value'] + "</h1>")


@app.route('/admin/users', methods=["GET", "POST"])
def index():
    if not check_admin():
        return redirect('/login')
    db.connect()
    if check_admin():
       return render_template('index.html', username=db.select_all_usernames("users"))


@app.route('/admin/edit/<username>')
def edit(username):
    if not check_admin():
        return redirect('/login')
    return render_template('edit.html', username=username)


@app.route('/admin/edit/modify', methods=['POST'])
def modify():
    if not check_admin():
        return redirect('/login')
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
    if not check_admin():
        return redirect('/login')
    return render_template('addUser.html')


@app.route('/admin/addUser/added', methods=['POST'])
def added():
    if not check_admin():
        return redirect('/login')
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
    if not check_admin():
        return redirect('/login')
    db.connect()
    username = request.form['username']
    username = username.strip()
    db.delete_user(username)
    db.close()
    return render_template('deleteSuccessful.html', username=username)


@app.route('/admin/delete', methods=['POST'])
def main_delete():
    if not check_admin():
        return redirect('/login')
    db.connect()
    username = request.form['username']
    username = username.strip()
    db.delete_user(username)
    return render_template('deleteSuccessful.html', username=username)
