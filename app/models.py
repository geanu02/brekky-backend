from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from secrets import token_urlsafe

from app import db, login

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    password = db.Column(db.String)
    token = db.Column(db.String(250), unique=True)
    user_recipe = db.relationship('UserRecipe', backref='recipe', lazy=True)

    def __repr__(self):
        return f"Registered Account: {self.email}"

    def commit(self):
        db.session.add(self)
        db.session.commit()

    def hash_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password_input):
        return check_password_hash(self.password, password_input)
    
    def add_token(self):
        setattr(self, 'token', token_urlsafe(32))

    def get_id(self):
        return str(self.user_id)
    
class UserRecipe(db.Model):
    user_recipe_id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer)
    recipe_title = db.Column(db.String(150))
    recipe_thumb = db.Column(db.String(250))
    recipe_api_content = db.Column(db.PickleType())
    recipe_user_content = db.Column(db.PickleType())
    recipe_api_url = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def commit(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"Registered UserRecipe: {self.user_recipe_id} ({self.recipe_title})>"