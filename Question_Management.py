from flask import Flask, render_template, redirect, url_for, request, flash , g, Blueprint, session
import sqlite3
from functools import wraps

Question_Management = Blueprint ("Question_Management", __name__, template_folder="templates")

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('quiz.db')
        g.db.row_factory = sqlite3.Row
        # print("Row factory is set")
    return g.db


def admin_required(f):
    @wraps(f)
    def decoratorrr(*args, **kwargs):
        if 'username' not in session or session['username'] != "admin":
            return render_template('not_allowed.html')
        else:
            return f(*args, **kwargs)
    return decoratorrr




@Question_Management.route('/questions/<category>')
@admin_required
def Question_manager(category):

    cursor = get_db().cursor()
    cursor.execute('SELECT * FROM questions WHERE category=?', (category,))
    filtered_questions = cursor.fetchall()
    return render_template('show_questions.html', Questions=filtered_questions, category=category)

    

@Question_Management.route('/categories')
@admin_required
def show_categories():

    cursor = get_db().cursor()
    cursor.execute('SELECT * FROM categories')
    categories = cursor.fetchall()

    return render_template('show_categories.html', categories=categories)



@Question_Management.route ('/questions/add/<category>', methods=['GET', 'POST'] )
@admin_required
def add_Question(category):

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



@Question_Management.route ('/questions/delet/<category>', methods = ['GET', 'POST'])
@admin_required
def remove_Question(category):

    cursor = get_db().cursor()
    if request.method == 'POST':

        selected_ids = request.form.getlist('id')
        for id in selected_ids:
            cursor.execute("DELETE FROM questions WHERE id=?",(id,))
        get_db().commit()

    cursor.execute("SELECT * FROM questions WHERE category=?", (category,))
    filtered_questions = cursor.fetchall()
    return render_template('delet_q.html', Questions=filtered_questions, category=category)



@Question_Management.route ('/categories/add', methods = ['GET', 'POST'])
@admin_required
def add_category():

    if request.method == 'POST':

        cursor = get_db().cursor()
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
            return redirect(url_for('Question_Management.Question_manager', category=new_category))

    return render_template('add_category.html')



@Question_Management.route ('/categories/delet/<category>')
@admin_required
def remove_category(category):

    cursor = get_db().cursor()
    cursor.execute("DELETE FROM questions WHERE category=?", (category,))
    cursor.execute("DELETE FROM categories WHERE name=?", (category,))
    get_db().commit()
    flash('Category Removed', 'danger')
    return redirect(url_for('Question_Management.show_categories'))

