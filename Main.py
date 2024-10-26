from flask import Flask, render_template, redirect, url_for, request, flash , g , session
import sqlite3
from Question_Management import Question_Management
from login_signup import login_signup


app = Flask (__name__)
app.register_blueprint(Question_Management, url_prefix="")
app.register_blueprint(login_signup, url_prefix="")
app.secret_key = 'fwugyewqlufywqliugfqw'


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('quiz.db')
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if exception:
        print(f'error: {exception}')
    if db is not None:
        db.close()




@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html')



if __name__ == '__main__':
    app.run (debug = False)