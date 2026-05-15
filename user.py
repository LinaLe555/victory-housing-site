from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from data import *

class User (UserMixin):
    def __init__(self, id):
       self.id = id
       self.username = id
       self.role = userbylogin(self.username)[2]
       
    @staticmethod
    def authenticate(username, password):
        user_data = userbylogin(username)
        if user_data and check_password_hash(user_data[3], password):
            return User(username)
        else:
            return None
    
    @staticmethod
    def get(username):
        user_data = userbylogin(username)
        if user_data:
            return User(username)
        else:
            return None
        
    def is_admin(self):
        return self.role == 'admin'
    

print(generate_password_hash('555'))