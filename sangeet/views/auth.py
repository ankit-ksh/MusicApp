# Implementing authentication

from flask import (
    Blueprint, redirect, render_template, request, session, url_for, flash
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import (
    login_user,
    logout_user,
    login_required,
)
from sangeet.models import *

bp = Blueprint('auth', __name__)

@bp.route('/')
def logged_out_home():
    return render_template('general/logged_out_homepage.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        # Server side validation for empty inputs
        if (user_name == "") or (password == ""):
            flash("Invalid Inputs", 'error')
        
        # finally query the database to find the user and log in
        alredy_user = db.session.execute(db.select(User).where(User.user_name == user_name)).scalar()
        if alredy_user:
            if password == alredy_user.password:
                login_user(alredy_user)
                return redirect(url_for('general.home'))
            else:
                flash('Incorrect Password!', 'error')
        else:
            flash('Username Not Found!', 'error')
    flash('Hello! Welcome back. User your User id and Password to log in. For any assistance contact us.')
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Succesfully Logged Out", 'success')
    return redirect(url_for('auth.login'))

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        user_name = request.form['user_name']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        try:
            isCreator = request.form['isCreator']
            role = 'creator'
        except:
            role = 'user'

        # Server side validation for empty inputs
        if (user_name == "") or (first_name == "") or (password == ""):
            flash('Invalid Input', 'error')
            return redirect(url_for('auth.register'))

        # Check if user_name already exists in database
        if db.session.execute(db.select(User).where(User.user_name == user_name)).scalar():
            flash('Username already exists. Try Another One!', 'error')
            return redirect(url_for('auth.register'))

        # if no user exist with these details, add the user data to database
        new_user = User(user_name=user_name, first_name=first_name, last_name=last_name, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('Account Created Succesfully! Log in Now', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@bp.route('/admin_login', methods=('GET', 'POST'))
def admin_login():
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        # Server side validation for empty inputs
        if (user_name == "") or (password == ""):
            flash("Invalid Inputs", 'error')
        
        # finally query the database to find the user and log in
        alredy_user = db.session.execute(db.select(User).where(User.user_name == user_name)).scalar()
        if alredy_user:
            if (password == alredy_user.password) and (alredy_user.role == 'admin'):
                login_user(alredy_user)
                return redirect(url_for('admin.home'))
            else:
                flash('Incorrect Password!', 'error')
        else:
            flash('No Admin with this username Found!', 'error')
    return render_template('/auth/admin_login.html')
