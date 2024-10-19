from flask import Flask, render_template, redirect, url_for

app = Flask (__name__)


#============================
Questions = [
    { 'Q' : '2+2' , 'A' : '4' },
    { 'Q' : '3+4' , 'A' : '7'}
]
#============================




@app.route ('/home/question/category')
def Question_manager():
    return render_template ('show_category.html', Questions = Questions)  # template question + botton add/remove
    

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