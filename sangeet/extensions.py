# extension for database - ORM flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# extension for authentication management - flask-login
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.blueprint_login_views = {
    'admin.admin_home': '/login/admin',
}
login_manager.login_message = 'You Need to Log in!'







# import functools

# from flask import (
#     Blueprint, flash, g, redirect, render_template, request, session, url_for
# )
# from werkzeug.security import check_password_hash, generate_password_hash
