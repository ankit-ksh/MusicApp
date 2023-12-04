# Implementing authentication

from flask import (
    Blueprint, redirect, render_template, request, session, url_for
)
from sangeet.extensions import db


bp = Blueprint('auth', __name__, template_folder='templates', static_folder='static', url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        user_name = request.form['user_name']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        pwd = request.form['password']

    return render_template('auth/register.html')

@bp.route('/user_login', methods=('GET', 'POST'))
def user_login():
    return render_template('auth/user_login.html')

@bp.route('/admin_login', methods=('GET', 'POST'))
def admin_login():
    return render_template('auth/admin_login.html')
