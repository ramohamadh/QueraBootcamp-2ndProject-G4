from flask import Flask, render_template, redirect, url_for, request, session, flash
import random

app = Flask(__name__)
app.secret_key = 'fwugyewqlufywqliugfqw'

# user list
users = [{'username': 'johndoe', 'password': 'hashed_password'}]

# categories list
categories = ['Mathematics', 'Science', 'History']

# questions list
questions = [
    {'category': 'Mathematics', 'question': '2 + 2 = ?', 'options': ['3', '4', '5'], 'answer': '4'},
    {'category': 'Mathematics', 'question': '5 * 3 = ?', 'options': ['15', '10', '20'], 'answer': '15'},
    {'category': 'Science', 'question': 'What planet is known as the Red Planet?', 'options': ['Earth', 'Mars', 'Venus'], 'answer': 'Mars'},
    {'category': 'History', 'question': 'Who was the first president of the United States?', 'options': ['Abraham Lincoln', 'George Washington', 'Thomas Jefferson'], 'answer': 'George Washington'}
]


results = []

# navigation bar
@app.route('/')
def index():
    return render_template('index.html')

# Categories
@app.route('/categories')
def show_categories():
    return render_template('categories.html', categories=categories)

# Select Number of Questions and Display Questions Randomly from Selected Category
@app.route('/quiz/<category>', methods=['GET', 'POST'])
def take_quiz(category):
    if request.method == 'POST':
        num_questions = int(request.form['num_questions'])
        
        # Filter Questions by Category and Select Questions Randomly
        selected_questions = [q for q in questions if q['category'] == category]
        random_questions = random.sample(selected_questions, min(num_questions, len(selected_questions)))

        # Save Questions for Use in the Next Stage
        session['quiz_questions'] = random_questions
        session['current_score'] = 0
        return redirect(url_for('quiz'))

    return render_template('select_num_questions.html', category=category)

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'quiz_questions' not in session:
        return redirect(url_for('show_categories'))
    
    quiz_questions = session['quiz_questions']
    current_score = session.get('current_score', 0)
    question_index = int(request.args.get('question_index', 0))
    
    if request.method == 'POST':
        user_answer = request.form['answer']
        question_index = int(request.form['question_index'])
        
        # Check Answer
        if user_answer == quiz_questions[question_index]['answer']:
            current_score += 1
        session['current_score'] = current_score

        # If Questions Are Finished, Redirect to Results Page
        if question_index + 1 >= len(quiz_questions):
            score = current_score
            results.append({'username': session.get('username', 'guest'), 'score': score})

            # Assign Feedback Based on Score
            if score == len(quiz_questions):
                feedback = "Excellent! You got everything right!"
            elif score > len(quiz_questions) / 2:
                feedback = "Well done! You did pretty good."
            else:
                feedback = "Needs Improvement. Better luck next time."

            flash(f'Your score is: {score}/{len(quiz_questions)}. {feedback}')
            return redirect(url_for('show_results'))
        
        question_index += 1

    # Check Question Index Limitation
    if question_index < len(quiz_questions):
        question = quiz_questions[question_index]
    else:
        return redirect(url_for('show_results'))

    return render_template('quiz.html', question=question, question_index=question_index, total=len(quiz_questions))


# Display Quiz Results
def show_results():
    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')