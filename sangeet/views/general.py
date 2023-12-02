# General Pages
from flask import (
    Blueprint, render_template
)
from sangeet.extensions import db

bp = Blueprint('homepage', __name__, template_folder='templates', static_folder='static', url_prefix='/')

@bp.route('/')
def logged_out_home():
    return render_template('general/logged_out_homepage.html')
