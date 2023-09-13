from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

   
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(150),unique = True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    admin= db.Column(db.String(100))
    
class Category(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100))
    categorys = db.relationship('Product', backref='category')
 
    
class Product(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100))
    expirydate=db.Column(db.String(100))
    price=db.Column(db.Integer)
    quantity=db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    products = db.relationship('Userbook', backref='product')
    
class Userbook(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    sname=db.Column(db.String(100))
    vname=db.Column(db.String(100))
    notickets=db.Column(db.Integer)
    total=db.Column(db.Integer)
    email = db.Column(db.String(150))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    
class Confirmbooking(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    pname=db.Column(db.String(100))
    cname=db.Column(db.String(100))
    quantity=db.Column(db.Integer)
    total=db.Column(db.Integer)
    overalltotal=db.Column(db.Integer)
    email = db.Column(db.String(150))

