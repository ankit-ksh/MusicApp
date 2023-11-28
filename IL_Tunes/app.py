from flask import (Flask, request, render_template, url_for, redirect)

app = Flask(__name__)

@app.route('/')
def user_home():
    return render_template('user/music_homepage.html')

@app.route('/register')
def register():
    return render_template('auth/register.html')

@app.route('/user_login')
def user_login():
    return render_template('auth/user_login.html')

@app.route('/admin_login')
def admin_login():
    return render_template('auth/admin_login.html')

@app.route('/creator_login')
def creator_login():
    return render_template('auth/creator_login.html')




if __name__ == '__main__':
    app.debug = True
    app.run()