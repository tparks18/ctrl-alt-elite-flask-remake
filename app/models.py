from click import password_option
from app import db, login
from flask_login import UserMixin #this is just for the user model
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, default=dt.utcnow)

    def __repr__(self):
        return f'<User: {self.id} | {self.email}>'

    #salts the password to make it hard to steal

    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    #compares the user password to the password privded in thhe login form

    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])

    #saves the user to the database
    def save(self):
        db.session.add(self) #add the user to the db session
        db.session.commit() #save everything in the session to the database

@login.user_loader
def load_user(id):
    return User.query.get(int(id)) #query coming from sqlalchemy

        #SELECT * FROM user WHERE id = ???