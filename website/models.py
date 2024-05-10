from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    
class MyTable(db.Model):
    __tablename__ = 'my_table'

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String)
    DOB = db.Column(String)
    gender = db.Column(String)
    aadhaarnumber = db.Column(String)
    state = db.Column(String)
    city = db.Column(String)
    pincode = db.Column(String)
    address = db.Column(String)
