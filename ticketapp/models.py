from __init__ import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True,autoincrement =True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name= db.Column(db.String(150))
    isadmin=db.Column(db.Boolean,default=False)

class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    admin_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(150))
    address = db.Column(db.String(150))
    city = db.Column(db.String(150))
    

class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
    name = db.Column(db.String(150))
    desc = db.Column(db.String(100))
    time=db.Column(db.Integer,nullable=False,default=func.now())
    price=db.Column(db.Integer,default=100)
    date = db.Column(db.String, nullable=False, default=func.now())
    capacity=db.Column(db.Integer)
    rating=db.Column(db.Integer)

class Booking(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    show_id=db.Column(db.Integer, db.ForeignKey('show.id'), nullable=False)
    tick=db.Column(db.Integer)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    show_id=db.Column(db.Integer, db.ForeignKey('show.id'))
    tag=db.Column(db.String(10))

    

