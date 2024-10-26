from flask import Flask, Blueprint, g, render_template, redirect, url_for, request, flash, session
import sqlite3

login_signup = Blueprint("login_signup", __name__, template_folder="templates")

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('quiz.db')
        g.db.row_factory = sqlite3.Row
    return g.db


@login_signup.route("/login_signup")
def login_or_signup():
    return render_template('signup_or_login.html')


@login_signup.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        input_username = request.form.get('username')
        input_password = request.form.get('password')
        
        cur = get_db().cursor()
        try:
            cur.execute('SELECT * FROM users WHERE username=?',(input_username,))
            hovered_user = cur.fetchone()
            if hovered_user and hovered_user['password'] == input_password:
                cur.execute("UPDATE users SET login=? WHERE username=?", (1, input_username))
                get_db().commit() 
                session['username'] = input_username
                flash('Successfull LogIn', 'success')
                return redirect(url_for('index'))
            elif hovered_user and hovered_user['password'] != input_password:
                flash('Wrong Password', 'danger')
                return render_template('login.html')
            else:
                flash('Wrong Username', 'danger')
                return render_template('login.html')   
        except sqlite3.Error as e:
            print(e)
            flash('Something went wrong, try again', 'danger')
            return render_template('login.html')


    return render_template('login.html')


@login_signup.route("/signup", methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        intended_username = request.form.get('username')
        intended_email = request.form.get('email')
        intended_password = request.form.get('password')

        cur = get_db().cursor()
        cur.execute("SELECT username, email FROM users")
        check_list = cur.fetchall()
        username_list = [username for (username,email,) in check_list]
        email_list = [email for (username,email,) in check_list]

        if intended_username not in username_list and intended_email not in email_list:
            cur.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                        (intended_username, intended_email, intended_password))  #mostaghim log in beshe ?
            get_db().commit()
            flash('Successfull SignUp', 'success')
            return render_template('signup_or_login.html')
        else:
            if intended_username in username_list and intended_email in email_list:
                flash('Username and Email not available', 'danger')
            elif intended_email in email_list:
                flash('Email not available', 'danger')
            elif intended_username in username_list:
                flash('Username not available', 'danger')
            return render_template('signup.html')
        
    return render_template('signup.html')


@login_signup.route('/logout/<username>')
def logout(username):
    cur = get_db().cursor()
    cur.execute("UPDATE users SET login=? WHERE username=?", (0, username))
    get_db().commit()
    session.pop('username', None)
    flash('Loged out Successfully', 'danger')
    return render_template('home.html')