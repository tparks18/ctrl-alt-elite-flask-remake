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
    icon = db.Column(db.Integer)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

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
        self.icon = data['icon']

    #saves the user to the database
    def save(self):
        db.session.add(self) #add the user to the db session
        db.session.commit() #save everything in the session to the database
    
    def get_icon_url(self):
        return f'https://avatars.dicebear.com/api/big-smile/{self.icon}.svg'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

        #SELECT * FROM user WHERE id = ???

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=dt.utcnow)
    date_updated = db.Column(db.DateTime, onupdate=dt.utcnow)
    user_id =  db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Post: {self.id} | {self.body[:15]}>'

    def edit(self):
        self.body = new_body

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    