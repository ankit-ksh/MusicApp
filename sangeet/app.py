from flask import (Flask, request, render_template, url_for, redirect)

app = Flask(__name__)

@app.route('/')
def user_home():
    return render_template('user/music_homepage.html')




@app.route('/creator_login')
def creator_login():
    return render_template('auth/creator_login.html')




if __name__ == '__main__':
    app.debug = True
    app.run()