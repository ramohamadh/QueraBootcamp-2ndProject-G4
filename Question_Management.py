from flask import Flask, render_template, redirect, url_for, request
from dataclasses import dataclass

app = Flask (__name__)


#============================
last_id = 7
Questions = [
    { 'id': '1', 'Q': '2+2', 'A': '4', 'category': 'Math' },
    { 'id': '2', 'Q': '3+4', 'A': '7', 'category': 'Math' },
    { 'id': '3', 'Q': 'Capital of France?', 'A': 'Paris', 'category': 'Geography' },
    { 'id': '4', 'Q': 'Author of Hamlet?', 'A': 'Shakespeare', 'category': 'Literature' },
    { 'id': '5', 'Q': 'Capital of England?', 'A': 'London', 'category': 'Geography' },
    { 'id': '6', 'Q': '10x10', 'A': '100', 'category': 'Math' },
    { 'id': '7', 'Q': '10/5', 'A': '2', 'category': 'Math' }
]
@dataclass
class User:
    username: str
    password: str
    is_login: bool
    role: str

Users = [User('admin', 'admin', True, 'admin')]
#============================


@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html')


@app.route('/questions/<category>')
def Question_manager(category):
    filtered_questions = [q for q in Questions if q['category'] == category]
    return render_template('show_questions.html', Questions=filtered_questions, category=category)
    

@app.route('/categories')
def show_categories():
    categories = {q['category'] for q in Questions}
    return render_template('show_categories.html', categories=categories)


@app.route ('/questions/add/<category>', methods=['GET', 'POST'] )
def add_Question(category):
    global Questions, last_id
    if request.method == 'POST':
        Question = request.form.get('question')
        Answer = request.form.get('answer')
        Category = category
        last_id += 1
        Questions.append({'id': last_id, 'Q': Question, 'A': Answer, 'category': Category})
    return render_template ('add_q.html', category=category)


@app.route ('/questions/delet/<category>', methods = ['GET', 'POST'])
def remove_Question(category):
    global Questions
    if request.method == 'POST':
        selected_ids = request.form.getlist('id')
        Questions = [q for q in Questions if str(q['id']) not in selected_ids]

    filtered_questions = [q for q in Questions if q['category'] == category]
    return render_template('delet_q.html', Questions=filtered_questions, category=category)


@app.route ('/categories/add')
def add_category():
    pass # template : html form baraye name of category

# remove category 




if __name__ == '__main__':
    app.run (debug = True)