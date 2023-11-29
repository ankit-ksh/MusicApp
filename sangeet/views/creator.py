# Implementing creator pages

from flask import (
    Blueprint, redirect, render_template, request, session, url_for
)
from sangeet.extensions import db

bp = Blueprint('auth', __name__, template_folder='templates', static_folder='static', url_prefix='/auth')
