from flask import Flask, render_template, redirect, url_for, request, flash
from dataclasses import dataclass

app = Flask (__name__)
app.secret_key = 'fwugyewqlufywqliugfqw'

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

current_user = User('admin', 'admin', True, 'admin')
#============================


@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html')


@app.route('/questions/<category>')
def Question_manager(category):
    if current_user.is_login:
        if current_user.role == 'admin':
            filtered_questions = [q for q in Questions if q['category'] == category]
            return render_template('show_questions.html', Questions=filtered_questions, category=category)
    else:
        return render_template ('not_allowed.html')
    

@app.route('/categories')
def show_categories():
    if current_user.is_login:
        if current_user.role == 'admin':
            categories = {q['category'] for q in Questions}
            return render_template('show_categories.html', categories=categories)
    else:
        return render_template ('not_allowed.html')


@app.route ('/questions/add/<category>', methods=['GET', 'POST'] )
def add_Question(category):
    global Questions, last_id
    if current_user.is_login:
        if current_user.role == 'admin':
            if request.method == 'POST':
                Question = request.form.get('question')
                Answer = request.form.get('answer')
                Category = category
                last_id += 1
                Questions.append({'id': last_id, 'Q': Question, 'A': Answer, 'category': Category})
                flash('Added Successfully', 'success')
            return render_template ('add_q.html', category=category)
    else:
        return render_template ('not_allowed.html')


@app.route ('/questions/delet/<category>', methods = ['GET', 'POST'])
def remove_Question(category):
    global Questions
    if current_user.is_login:
        if current_user.role == 'admin':
            if request.method == 'POST':
                selected_ids = request.form.getlist('id')
                Questions = [q for q in Questions if str(q['id']) not in selected_ids]

            filtered_questions = [q for q in Questions if q['category'] == category]
            return render_template('delet_q.html', Questions=filtered_questions, category=category)
    else:
        return render_template ('not_allowed.html')


@app.route ('/categories/add', methods = ['GET', 'POST'])
def add_category():
    if current_user.is_login:
        if current_user.role == 'admin':
            if request.method == 'POST':

                new_category=request.form.get('category')
                if next((True for q in Questions if q['category'] == new_category),False):
                    flash('This category already exist', 'danger')
                else:
                    flash('Successfully created new category', 'success')
                    return redirect(url_for('Question_manager', category=new_category))
    
            return render_template('add_category.html')
    else:
        return render_template ('not_allowed.html')


@app.route ('/categories/delet/<category>')
def remove_category(category):
    global Questions
    if current_user.is_login:
        if current_user.role == 'admin':
            Questions = [q for q in Questions if q['category'] != category]
            flash('Category Removed', 'danger')
            return redirect(url_for('show_categories'))
    else:
        return render_template ('not_allowed.html')



if __name__ == '__main__':
    app.run (debug = False)