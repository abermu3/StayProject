from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.dog import Dog
from flask_app.models.user import User
from flask_app.config.mysqlconnection import connectToMySQL
import datetime



@app.route('/new/dog', methods=['POST'])
def addDog():
    if 'user_id' not in session:
        return redirect('/')
    if not Dog.validate_dog(request.form):
        return redirect('/add')
    switchVal= request.form.get('checked_in')
    if switchVal== 'on':
        switchVal= 1
        dog_data= {
        'user_id': session['user_id'],
        'checked_in': switchVal,
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'breed': request.form['breed'],
        'kennel': request.form['kennel'],
        'allergies': request.form['allergies'],
        'feeding_notes': request.form['feeding_notes'],
        'med_notes': request.form['med_notes'],
        'daily_care': request.form['daily_care'],
        'return_items': '',
        'checkout': request.form['checkout']
    }
    else:
        switchVal= 0
        dog_data= {
        'user_id': session['user_id'],
        'checked_in': switchVal,
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'breed': request.form['breed'],
        'kennel': '',
        'allergies': request.form['allergies'],
        'feeding_notes': request.form['feeding_notes'],
        'med_notes': request.form['med_notes'],
        'daily_care': request.form['daily_care'],
        'return_items': '',
        'checkout': None
    }
    
    Dog.save_dog(dog_data)
    return redirect('/home')

@app.route('/add')
def newDog():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('add_dog.html')

@app.route('/dog/<int:id>')
def viewDog(id):
    if 'user_id' not in session:
        return redirect('/')
    user= User.get_by_id({'id':session['user_id']})
    return render_template('view_dog.html', user=user, dog= Dog.get_by_id({'id': id}))

@app.route('/edit/<int:id>')
def editPage(id):
    if 'user_id' not in session:
        return redirect('/')
    return render_template('edit_dog.html', dog= Dog.get_by_id({'id': id}))

@app.route('/edit/dog/<int:id>', methods= ['POST'])
def editDog(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Dog.validate_dog(request.form):
        return redirect(f'/edit/{id}')
    switchVal= request.form.get('checked_in')
    if switchVal== 'on':
        switchVal= 1
    else:
        switchVal= 0
    dog_data= {
        'id': id,
        'checked_in': switchVal,
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'breed': request.form['breed'],
        'kennel': request.form['kennel'],
        'allergies': request.form['allergies'],
        'feeding_notes': request.form['feeding_notes'],
        'med_notes': request.form['med_notes'],
        'daily_care': request.form['daily_care'],
        'return_items': '',
        'checkout': request.form['checkout']

    }
    Dog.update(dog_data)
    return redirect('/home')



@app.route('/search', methods=['GET','POST'])
def search():
    if 'user_id' not in session:
        return redirect('/')
    if request.method== 'POST':
        db= connectToMySQL('stay_dogs')
        search= request.form['search']
        query= "SELECT * FROM dogs WHERE LOWER(first_name) LIKE LOWER(%s) OR LOWER(last_name) LIKE LOWER(%s)"
        results= db.query_db(query, ('%' + search + '%', '%' + search + '%',))
        return render_template('search_results.html', dogs=results)

@app.route('/edit/status/<int:id>', methods= ['POST'])
def inOrOut(id):
    if 'user_id' not in session:
        return redirect('/')
    switchVal= request.form.get('checked_in')
    if switchVal== 'on':
        switchVal= 1
        dog_data= {
        'id': id,
        'checked_in': switchVal,
        'return_items': '',
        'kennel': request.form['kennel'],
        'checkout': request.form['checkout']
    }
    else:
        switchVal= 0
        dog_data= {
        'id': id,
        'checked_in': switchVal,
        'kennel': '',
        'return_items': '',
        'checkout': None
    }
    
    Dog.updateStatus(dog_data)
    return redirect('/home')

@app.route('/items')
def checkoutItemsPage():
    if 'user_id' not in session:
        return redirect('/')
    today= datetime.date.today()
    return render_template('checkout_items_page.html', dogs= Dog.get_all(), dog= Dog.get_by_id({'id': id}), today=today)

@app.route('/return/item', methods=['POST'])
def checkoutItems():
    if 'user_id' not in session:
        return redirect('/')
    dog_data= {
        'id': request.form['id'],
        'return_items': request.form['return_items']
    }
    Dog.returnItems(dog_data)
    return redirect('/items')

@app.route('/returned', methods=['POST'])
def checkOff():
    if 'user_id' not in session:
        return redirect('/')
    dog_data= {
            'id': request.form['id'],
            'return_items': ''
        }
    Dog.returnItems(dog_data)
    return redirect('items')

@app.route('/delete/<int:id>')
def destroy(id):
    if 'user_id' not in session:
        return redirect('/')
    Dog.delete({'id': id})
    return redirect('/home')


