# Implementing authentication

from flask import (
    Blueprint, redirect, render_template, request, session, url_for
)
from sangeet.extensions import db


bp = Blueprint('auth', __name__, template_folder='templates', static_folder='static', url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    return render_template('auth/register.html')

@bp.route('/user_login', methods=('GET', 'POST'))
def user_login():
    return render_template('auth/user_login.html')

@bp.route('/admin_login', methods=('GET', 'POST'))
def admin_login():
    return render_template('auth/admin_login.html')
