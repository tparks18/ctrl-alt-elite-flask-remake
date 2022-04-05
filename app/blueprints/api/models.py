from app import db
from datetime import datetime as dt

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    desc = db.Column(db.Text)
    price = db.Column(db.Float)
    img = db.Column(db.String)
    created_on = db.Column(db.DateTime, index=True, default=dt.utcnow)
    category_id = db.Column(db.ForeignKey('category.id'))

    def __repr__(self):
        return f'<Item: {self.id} | {self.name}>'

    def to_dict(self):
        data={
            "id": self.id,
            "name": self.name,
            "desc": self.desc,
            "price": self.price,
            "img": self.img,
            "created_on": self.created_on,
            "category_id": self.category_id,
            "category_name": self.cat.name
        }
        return data

    def from_dict(self,data):
        for field in ["name", "desc", "price", "img", "category_id"]:
            if field in data:
                #the object, the attribute, value
                setattr(self, field, data[field])

    def save(self):
        db.session.add(self) # add the user to the db session
        db.session.commit() #save everything in the session to the database

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    products = db.relationship('Item', cascade='all, delete-orphan', backref='cat', lazy='dynamic')

    def __repr__(self):
        return f'<Category: {self.id} | {self.name}>'

    # saves the post to the database
    def save(self):
        db.session.add(self) # add the user to the db session
        db.session.commit() #save everything in the session to the database

    def delete(self):
            db.session.delete(self)
            db.session.commit()

    def to_dict(self):
        data={
            "id": self.id,
            "name": self.name
        }
        return data