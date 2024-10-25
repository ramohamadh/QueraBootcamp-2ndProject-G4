from flask import Flask, render_template, redirect, url_for, request, flash , g
from dataclasses import dataclass
import sqlite3

app = Flask (__name__)
app.secret_key = 'fwugyewqlufywqliugfqw'



def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('quiz.db')
        g.db.row_factory = sqlite3.Row
        # print("Row factory is set")
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if exception:
        print(f'error: {exception}')
    if db is not None:
        db.close()

#==================
@app.route('/currentUser')
def get_current_user(user: str):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE users SET login=? WHERE username=?', (True, user))
    cursor.execute('SELECT * FROM users WHERE username = ?', (user,))
    current_user = cursor.fetchone()
    return current_user


def admin_check(user):

    current_user = get_current_user(user)

    if current_user['login'] == 1:
        if current_user['admin'] == 1:
            return True
    return False
#===========================





@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html')


@app.route('/questions/<category>')
def Question_manager(category):
    if admin_check('admin'):
        cursor = get_db().cursor()
        cursor.execute('SELECT * FROM questions WHERE category=?', (category,))
        filtered_questions = cursor.fetchall()
        return render_template('show_questions.html', Questions=filtered_questions, category=category)
    else:
        return render_template ('not_allowed.html')
    

@app.route('/categories')
def show_categories():
    if admin_check('admin'):
        cursor = get_db().cursor()
        cursor.execute('SELECT * FROM categories')
        categories = cursor.fetchall()

        return render_template('show_categories.html', categories=categories)
    else:
        return render_template ('not_allowed.html')


@app.route ('/questions/add/<category>', methods=['GET', 'POST'] )
def add_Question(category):
    if admin_check('admin'):
        if request.method == 'POST':
            Question = request.form.get('question')
            Answer = request.form.get('answer')
            Category = category
            cursor = get_db().cursor()
            cursor.execute("INSERT INTO questions (category, question, answer) VALUES (?, ?, ?)",
                (Category, Question, Answer))
            get_db().commit()
            flash('Added Successfully', 'success')
        return render_template ('add_q.html', category=category)
    else:
        return render_template ('not_allowed.html')


@app.route ('/questions/delet/<category>', methods = ['GET', 'POST'])
def remove_Question(category):
    if admin_check('admin'):
        cursor = get_db().cursor()
        if request.method == 'POST':
            selected_ids = request.form.getlist('id')
            for id in selected_ids:
                cursor.execute("DELETE FROM questions WHERE id=?",(id,))
            get_db().commit()

        cursor.execute("SELECT * FROM questions WHERE category=?", (category,))
        filtered_questions = cursor.fetchall()
        return render_template('delet_q.html', Questions=filtered_questions, category=category)
    else:
        return render_template ('not_allowed.html')


@app.route ('/categories/add', methods = ['GET', 'POST'])
def add_category():
    cursor = get_db().cursor()
    if admin_check('admin'):
        if request.method == 'POST':

            new_category=request.form.get('category')
            cursor.execute("SELECT name FROM categories")
            category_rows = cursor.fetchall()
            categories = [category for (category,) in category_rows]
            if next((True for category in categories if category == new_category),False):
                flash('This category already exist', 'danger')
            else:
                cursor.execute("INSERT INTO categories (name) VALUES (?)", (new_category,))
                get_db().commit()
                flash('Successfully created new category', 'success')
                return redirect(url_for('Question_manager', category=new_category))

        return render_template('add_category.html')
    else:
        return render_template ('not_allowed.html')


@app.route ('/categories/delet/<category>')
def remove_category(category):
    cursor = get_db().cursor()
    if admin_check('admin'):
            cursor.execute("DELETE FROM questions WHERE category=?", (category,))
            cursor.execute("DELETE FROM categories WHERE name=?", (category,))
            get_db().commit()
            flash('Category Removed', 'danger')
            return redirect(url_for('show_categories'))
    else:
        return render_template ('not_allowed.html')

#---------------------------------------------------------------------------------------------------------------------------------
user_data = {
    'name': 'username',
    'last_name': 'user lastname',
    'email': 'user@email.com',
    'age': 30,
    'username': 'user123',
    'password': '1234',
    'marks': [10, 8 , 7 ,5, 9]
}

@app.route('/profile')
def profile():
    return render_template('profile.html', user=user_data)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if request.method == 'POST':
        user_data['name'] = request.form['name']
        user_data['last_name'] = request.form['last_name']
        user_data['email'] = request.form['email']
        user_data['age'] = request.form['age']
        print(user_data['password'])

        password = request.form.get('password')
        if password:
            user_data['password'] = password
            print(user_data['password']) #something
            pass
        
        flash('Profile updated successfully !', 'success')
        return redirect(url_for('profile'))

    return render_template('edit_profile.html', user=user_data)

@app.route('/quiz_marks')
def quiz_marks():
    return render_template('quiz_marks.html', marks=user_data['marks'])

#-----------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run (debug = False)