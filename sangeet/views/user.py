# Implementing user pages

from flask import (
    Blueprint, redirect, render_template, request, session, url_for
)
from sangeet.extensions import db

bp = Blueprint('user', __name__, template_folder='templates', static_folder='static', url_prefix='/user')

@bp.route('/home')
def home():
    return render_template('user/home.html')


