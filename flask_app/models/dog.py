from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash


class Dog:
    DB="stay_dogs"

    def __init__(self,data):
       self.id= data['id']
       self.checked_in= data['checked_in']
       self.first_name= data['first_name']
       self.last_name= data['last_name']
       self.breed= data['breed']
       self.kennel= data['kennel']
       self.allergies= data['allergies']
       self.feeding_notes= data['feeding_notes']
       self.med_notes= data['med_notes']
       self.daily_care= data['daily_care']
       self.return_items= data['return_items']
       self.checkout= data['checkout']
       self.created_at= data['created_at']
       self.updated_at= data['updated_at']
       self.user_id= data['user_id']
       self.creator= None

    @classmethod
    def save_dog(cls,data):
        query= "INSERT INTO dogs(checked_in, first_name, last_name, breed, kennel, allergies, feeding_notes, med_notes, daily_care, return_items, checkout, user_id) VALUES(%(checked_in)s, %(first_name)s, %(last_name)s, %(breed)s,%(kennel)s,%(allergies)s, %(feeding_notes)s,%(med_notes)s,%(daily_care)s,%(return_items)s,%(checkout)s, %(user_id)s);"
        result= connectToMySQL("stay_dogs").query_db(query,data)
        return result
    
    @classmethod 
    def get_all(cls):
        query= "SELECT * FROM dogs JOIN users ON dogs.user_id= users.id;"
        results= connectToMySQL("stay_dogs").query_db(query)
        dogs= []
        for row in results:
            this_dog= cls(row)
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': '',
                'admin': row['admin'],
                'confirmed': row['confirmed'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']

            }
            this_dog.creator= user.User(user_data)
            dogs.append(this_dog)
        return dogs
    
    @classmethod
    def get_by_id(cls,data):
        query= "SELECT * FROM dogs JOIN users ON dogs.user_id= users.id WHERE dogs.id=%(id)s;"
        results= connectToMySQL("stay_dogs").query_db(query,data)
        if not results:
            return False
        results= results[0]
        this_dog= cls(results)
        user_data= {
                'id': results['users.id'],
                'first_name': results['first_name'],
                'last_name': results['last_name'],
                'email': results['email'],
                'password': '',
                'admin': results['admin'],
                'confirmed': results['confirmed'],
                'created_at': results['created_at'],
                'updated_at': results['updated_at']
        }
        this_dog.creator= user.User(user_data)
        return this_dog
    
    @classmethod
    def update(cls, data):
        query= "UPDATE dogs SET checked_in= %(checked_in)s, first_name= %(first_name)s, last_name= %(last_name)s, breed= %(breed)s, kennel= %(kennel)s, allergies= %(allergies)s, feeding_notes= %(feeding_notes)s, med_notes= %(med_notes)s, daily_care= %(daily_care)s, return_items= %(return_items)s, checkout= %(checkout)s WHERE id= %(id)s;"
        result= connectToMySQL("stay_dogs").query_db(query,data)
        return result
    
    @classmethod
    def updateStatus(cls, data):
        query= "UPDATE dogs SET checked_in= %(checked_in)s, kennel= %(kennel)s, return_items= %(return_items)s, checkout= %(checkout)s WHERE id= %(id)s;"
        result= connectToMySQL("stay_dogs").query_db(query,data)
        return result
    
    @classmethod
    def returnItems(cls, data):
        query= "UPDATE dogs SET return_items= %(return_items)s WHERE id= %(id)s;"
        result= connectToMySQL("stay_dogs").query_db(query,data)
        return result
    
    @classmethod
    def delete(cls, data):
        query= "DELETE FROM dogs WHERE id= %(id)s;"
        result= connectToMySQL("stay_dogs").query_db(query,data)
        return result
    
    @staticmethod
    def validate_dog(data):
        is_valid= True 
        if len(data['first_name']) < 1:
            flash("First name cannot be blank.")
            is_valid= False
        if len(data['last_name']) < 1:
            flash("Last name cannot be blank.")
            is_valid= False
        if len(data['breed']) < 1:
            flash("Breed required.")
            is_valid= False
        return is_valid
    @staticmethod
    def validate_checkin(data):
        is_valid= True 
        if len(data['kennel']) < 1:
            flash("Kennel number required")
            is_valid= False
        if not(data['checkour']):
            flash("Checkout day required")
            is_valid= False
        return is_valid