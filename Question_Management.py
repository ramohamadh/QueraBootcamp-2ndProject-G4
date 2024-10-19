from flask import Flask, render_template, redirect, url_for

app = Flask (__name__)


#============================
Questions = [
    { 'Q': '2+2', 'A': '4', 'category': 'Math' },
    { 'Q': '3+4', 'A': '7', 'category': 'Math' },
    { 'Q': 'Capital of France?', 'A': 'Paris', 'category': 'Geography' },
    { 'Q': 'Author of Hamlet?', 'A': 'Shakespeare', 'category': 'Literature' }
]
#============================




@app.route('/home/question/show_question/<category>')
def Question_manager(category):
    filtered_questions = [q for q in Questions if q['category'] == category]
    return render_template('show_questions.html', Questions=filtered_questions, category=category)  # template question + botton add/remove
    


@app.route('/home/question/categories')
def show_categories():
    categories = {q['category'] for q in Questions}
    return render_template('show_categories.html', categories=categories)



@app.route ('/home/question/<category>/add')
def add_Question():
    pass # 

@app.route ('/home/question/<category>/delet')
def remove_Question():
    pass # if len > 0

@app.route ('/home/question/add_category')
def add_category():
    pass # template : html form baraye name of category

# remove category 




if __name__ == '__main__':
    app.run (debug = False)