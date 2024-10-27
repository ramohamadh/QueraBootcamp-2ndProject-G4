from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3
import random
from functools import wraps

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database connection
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('quiz.db')
        g.db.row_factory = sqlite3.Row  # Fetch rows as dictionaries
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Fetch all quiz categories from the database
def get_categories():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT name FROM categories")
    categories = [row['name'] for row in cursor.fetchall()]
    return categories

# Fetch questions for a specific category
def get_questions(category):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT question, answer FROM questions WHERE category = ?", (category,))
    questions = cursor.fetchall()
    return [{'question': row['question'], 'options': [], 'answer': row['answer']} for row in questions]

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decoratorrr(*args, **kwargs):
        if 'username' not in session or session['username'] != "admin":
            return render_template('not_allowed.html')
        else:
            return f(*args, **kwargs)
    return decoratorrr

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Show quiz categories
@app.route('/categories')
def show_categories():
    categories = get_categories()  # Fetch categories from the database
    return render_template('categories.html', categories=categories)

# Start quiz based on selected category
@app.route('/quiz/<category>', methods=['GET', 'POST'])
def start_quiz(category):
    if request.method == 'POST':
        num_questions = int(request.form.get('num_questions'))
        session['category'] = category
        session['num_questions'] = num_questions
        session['score'] = 0
        questions = get_questions(category)
        selected_questions = random.sample(questions, min(num_questions, len(questions)))  # Ensure we don't exceed available questions
        session['questions'] = selected_questions
        session['current_question'] = 0
        return redirect(url_for('quiz'))
    return render_template('select_num_questions.html', category=category)

# Show quiz questions
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'questions' not in session or session['current_question'] >= session['num_questions']:
        return redirect(url_for('show_result'))
    
    question = session['questions'][session['current_question']]
    if request.method == 'POST':
        answer = request.form.get('answer')
        if answer == question['answer']:
            session['score'] += 1
        session['current_question'] += 1
        return redirect(url_for('quiz'))
    
    return render_template('quiz.html', question=question, question_num=session['current_question'] + 1)

# Show final result
@app.route('/result')
def show_result():
    score = session.get('score', 0)
    num_questions = session.get('num_questions', 0)
    feedback = f"Your score is {score} out of {num_questions}."
    return render_template('result.html', score=score, feedback=feedback)

if __name__ == '__main__':
    app.run(debug=True)