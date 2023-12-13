from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import bcrypt
import re



EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    DB="stay_dogs"

    def __init__(self,data):
        self.id= data['id']
        self.first_name= data['first_name']
        self.last_name= data['last_name']
        self.email= data['email']
        self.password= data['password']
        self.admin= data['admin']
        self.confirmed= data['confirmed']
        self.created_at= data['created_at']
        self.updated_at= data['updated_at']
        
    @classmethod
    def save_user(cls,form):
        
        hash_data= {
            'first_name': form['first_name'],
            'last_name': form['last_name'],
            'email': form['email'],
            'password': bcrypt.generate_password_hash(form['password']),
            'admin': False,
            'confirmed': False

        }
        query= "INSERT INTO users(first_name, last_name, email, password, admin, confirmed) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(admin)s, %(confirmed)s);"
        result= connectToMySQL("stay_dogs").query_db(query,hash_data)
        return result
    
    @classmethod 
    def updateConfirmation(cls, form):
        query= "UPDATE users SET confirmation= %(confirmation)s WHERE id= %(id)s;"
        result= connectToMySQL("stay_dogs").query_db(query)
        return result
    
    @classmethod 
    def get_all(cls):
        query= """SELECT * FROM users;"""
        results= connectToMySQL("stay_dogs").query_db(query)
        users= []
        for u in results:
            users.append(cls(u))
        return users
    
    @classmethod
    def get_by_email(cls, data):
        query= "SELECT * FROM users WHERE email= %(email)s;"
        result= connectToMySQL("stay_dogs").query_db(query,data)
        if not result:
            return False
        return cls(result[0])
    
    @classmethod
    def get_by_id(cls,data):
        query= "SELECT * FROM users WHERE id= %(id)s;"
        result= connectToMySQL("stay_dogs").query_db(query,data)
        if not result:
            return False
        return cls(result[0])

    @staticmethod
    def validate_user(form_data):
        is_valid = True
        if len(form_data['first_name']) < 1:
            flash("Required Field: First Name")
            is_valid= False
        elif len(form_data['first_name']) < 2:
            flash("First Name must be at least 2 characters.")
            is_valid = False
        if len(form_data['last_name']) < 1:
            flash("Required Field: Last Name")
            is_valid = False
        elif len(form_data['last_name']) < 2:
            flash("Last Name must be at least 2 characters.")
            is_valid = False
        if len(form_data['email']) < 1:
            flash("Required Field: Email")
            is_valid = False
        elif not EMAIL_REGEX.match(form_data['email']):
            flash("Invalid email address.")
            is_valid = False
        elif User.get_by_email(form_data):
            flash("User already exists.")
            is_valid= False
        if len(form_data['password']) < 13:
            flash("Password must be at least 13 characters long.")
            is_valid = False
        if form_data['password'] != form_data['confirm_password']:
            flash("Passwords do not match.")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(form):
        if not EMAIL_REGEX.match(form['email']):
            flash("Invalid email/password.")
            return False

        user = User.get_by_email(form)
    
        if not user:
            flash("Invalid email/password.")
            return False
        
        if not bcrypt.check_password_hash(user.password, form['password']):
            flash("Invalid email/password.")
            return False
        
        return user