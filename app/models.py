from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()



addproduct = db.Table('cart',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.item_id'), primary_key=True)
)


class  User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False, unique=True)
    last_name = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(45), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    cart = db.relationship("Product",
        secondary = addproduct,
        backref=db.backref('addtocart', lazy='dynamic'),
        
        lazy='dynamic'

    )
    

    def __init__(self, first_name, last_name, username, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def saveToCart(self, product):
        self.cart.append(product) # what does save mean?
        db.session.commit()

    def deleteFromCart(self, product): ## why is this method in the user class?
        # self.cart.delete(user)
        self.cart.remove(product) ## should we add a deleteEntireCart method? (is it better to delete via the models or via the route?) (if models, we could use a from user TRUNCATE TABLE method...)
        db.session.commit()

    def deleteAllFromCart(self):        
        for item in self.cart:
            self.cart.remove(item)
        # db.session.query(self.cart).delete()
        db.session.commit()


class  Product(db.Model):
    __tablename__= 'product'
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(1000), nullable=False, unique=True)
    img_url = db.Column(db.String(1000), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)

    


    def __init__(self, item_name,img_url,price):
        self.item_name = item_name
        self.img_url = img_url
        self.price = price
  

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.item_id,
            'item_name': self.item_name,
            'img_url': self.img_url,
            'price': self.price
        }