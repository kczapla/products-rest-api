from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)


class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String()) 
    brand = db.Column(db.String())
    category = db.Column(db.String())
    price = db.Column(db.Numeric())


    def __init__(self, name, brand, category, price):

        self.name = name
        self.brand = brand
        self.category = category
        self.price = price

    def __repr__(self):
        return 'name {}, price {}'.format(self.name, self.price)

@app.route('/')
def index():
    return "hello"

@app.route('/articles', methods=['GET'])
def get_articles():
    products = Products.query.all()
    return products


if __name__ == '__main__':
    app.run()
