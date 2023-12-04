from datetime import datetime
from app import db


cart_association = db.Table('cart_association',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(100), nullable=False)

    cart = db.relationship('Product', secondary=cart_association, back_populates='users_in_cart')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.phone}', '{self.address}')"
    

    def is_active(self):
        return True
    

    def get_id(self):
        return str(self.id)
    

    def is_authenticated(self):
        return True
    

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)

    users_in_cart = db.relationship('User', secondary=cart_association, back_populates='cart')

    def __repr__(self):
        return f"Product('{self.name}', '{self.quantity}', '{self.price}', '{self.description}', '{self.ingredients}')"