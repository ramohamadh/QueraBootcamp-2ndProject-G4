from flask import Flask, render_template, redirect, url_for, request, flash , g, Blueprint, session , abort
import sqlite3
from functools import wraps

profile1 = Blueprint ("profile1", __name__, template_folder="templates")

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('quiz.db')
        g.db.row_factory = sqlite3.Row
    return g.db


@profile1.route('/profile/<username>')
def profile(username):
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()

    if user is None:
        abort(404)  #404 error
        
    return render_template('profile.html', user=user)


@profile1.route('/edit_profile/<username>', methods=['GET', 'POST'])
def edit_profile(username):
    conn = get_db()

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        age = request.form['age']
        password = request.form['password']

        conn.execute('UPDATE users SET first_name = ?, last_name = ?, email = ?, age = ?, password = ? WHERE username = ?',
                     (first_name, last_name, email, age, password, username))
        conn.commit()
        conn.close()
        return redirect(url_for('profile1.profile', username=username))

    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()

    if user is None:
        abort(404)

    return render_template('edit_profile.html', user=user)


@profile1.route('/quiz_marks/<username>')
def quiz_marks(username):
    conn = get_db()
    #fetch
    user = conn.execute('SELECT * FROM users WHERE Username = ?', (username,)).fetchone()
    conn.close()

    if user is None:
        abort(404)

    #quiz list
    quiz_marks = user['quiz_results'].split(',') if user['quiz_results'] else []

    return render_template('quiz_marks.html', username=username, marks=quiz_marks)
