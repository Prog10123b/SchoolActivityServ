from app.main import bp
from app.main.models import User
from app.extensions import db

from flask import render_template, request, redirect, url_for, make_response
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.utils import secure_filename

import os

from app.main import config

@bp.route('/')
def index():
    return render_template('homepage.html')

@bp.route('/konkurs_talantov')
def konkurs_talantov():
    return render_template('konkurs_talantov.html')

@bp.route('/konkurs_talantov/login', methods=['GET', 'POST'])
def konkurs_talantov_login():
    if request.method == 'POST':
        useremail = request.form['email']
        userpass = request.form['password']
        
        print(f'New user login with {useremail}')

        try:
            user = db.session.execute(db.select(User).filter_by(email=useremail)).scalar_one()
        except:
            return 'Wrong username or password'

        if user.check_pass(userpass):
            resp = make_response(redirect(url_for('main.konkurs_talantov_cabinet'), 301))
            
            login_user(user)
            return redirect(url_for('main.konkurs_talantov_cabinet'), 301)
        else:
            return 'Wrong username or password'
        
    else:
        return render_template('konkurs_talantov_login.html')

@bp.route('/konkurs_talantov/register', methods=['GET', 'POST'])
def konkurs_talantov_register():
    if request.method == 'POST':
        username = request.form['name']
        usersurname = request.form['surname']
        useremail = request.form['email']
        userpass = request.form['password']
        userpassvalid = request.form['validation']
        
        print(f'New user register with {useremail}')

        if userpass != userpassvalid:
            return 'Passwords must match!'

        user = None

        try:
            user = db.session.execute(db.select(User).filter_by(email=useremail)).scalar_one()
        except:
            pass
        
        if user:
            return 'Error! this email is unavailable!'

        try:
            user = User(useremail, userpass, username, usersurname)
            db.session.add(user)
            db.session.commit()

            login_user(user)
            return redirect(url_for('main.konkurs_talantov_cabinet'), 301)
        except:
            return 'Unexpected error! Maybe this email is unavailable or too long.'
    else:
        return render_template('konkurs_talantov_register.html')


def check_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

@bp.route('/konkurs_talantov/cabinet', methods=['GET', 'POST'])
@login_required
def konkurs_talantov_cabinet():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'Could not read the file.'

        file = request.files['file']

        if file.filename == '':
            return 'No file selected.'

        if file and check_file(file.filename):

            filename = secure_filename(file.filename)

            new_path = os.getcwd() + config.UPLOAD_FOLDER + f'\\{current_user.id}\\'

            if not os.path.exists(new_path):    os.mkdir(new_path)

            file.save(os.path.join(new_path, filename))

            return 'Saved!'
        else:
            return 'File is not allowed!'
            
    else:
        return render_template('konkurs_talantov_cabinet.html')

@bp.route('/konkurs_talantov/logout')
@login_required
def konkurs_talantov_logout():
    logout_user()
    return redirect(url_for('main.konkurs_talantov'), 301)
