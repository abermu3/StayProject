from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.dog import Dog

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/signup')
def register():
    return render_template('register.html')

@app.route('/new/user', methods= ['POST'])
def create_user():
    if not User.validate_user(request.form):
        return redirect('/signup')
    user_id= User.save_user(request.form)
    session['user_id'] = user_id
    return redirect('/home')

@app.route('/login', methods= ['POST'])
def loginForm():
    user_in_db= User.validate_login(request.form)
    if not user_in_db:
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/home')

@app.route('/home')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    user= User.get_by_id({'id':session['user_id']})
    if not user:
        return redirect('/')
    dogs= Dog.get_all()
    return render_template('home.html', user=user, dogs=dogs)

@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id')
    return redirect('/')
