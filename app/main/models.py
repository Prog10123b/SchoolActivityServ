from app.extensions import db

from flask_login import UserMixin

import hashlib
import string
import random


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(32))
    password_salt = db.Column(db.String(8))
    firstname = db.Column(db.String(20))
    surname = db.Column(db.String(50))
    

    def __init__(self, email, password, name, surname):
        self.email = email
        self.firstname = name
        self.surname = surname

        salt = ''.join(random.choices(string.ascii_letters+string.digits, k=8))
        self.password_hash = hashlib.md5((password + salt).encode()).hexdigest()
        self.password_salt = salt

    def __repr__(self):
        return f'<User {self.email}>'

    def check_pass(self, password):
        tmp_hash = hashlib.md5((password + self.password_salt).encode()).hexdigest()
        return tmp_hash == self.password_hash

    def get_salt_hash(self):
        return hashlib.md5(self.password_salt.encode()).hexdigest()
