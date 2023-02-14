from flask import Blueprint, request
import requests
from ...models import Product, User
from ..apiauthhelper import basic_auth
from flask_login import current_user, login_required
from flask_cors import cross_origin

api = Blueprint('api', __name__)

@api.route('/api/populate')
def populate():

    url = "https://api.nasa.gov/planetary/apod?api_key=kFHR3AFVVyE6UWjaIGXtd1dHO4ey1Z9SZcGlG6J0&start_date=2022-12-01&end_date=2023-01-01"

    monthly_apod = {}

    response = requests.get(url)
    if response.status_code == 200:
        apod_month_list = response.json()
        # print(apod_month_list)
        for apod in apod_month_list:
            monthly_apod['item_name'] = apod['title']
            monthly_apod['img_url'] = apod['url']
            monthly_apod['price'] = 20 # RNG here next

            item_name = monthly_apod['item_name']
            img_url = monthly_apod['img_url']
            price =  monthly_apod['price']

            product = Product(item_name, img_url, price)
            product.saveToDB()
            continue
            
    posts = Product.query.all()
    print(posts)

    return {
        'status': 'ok',
        'totalResults': len(posts),
        'posts': [p.to_dict() for p in posts]
    }
    
@api.route('/api/')
@login_required
def homePage():
    posts = Product.query.all()
    print(posts)
    return {
        'status': 'ok',
    }

@api.route('/api/all_products')
def displayAllProducts():
    
    posts = Product.query.all()
    print(posts)
    return {
        'status': 'ok',
        'totalResults': len(posts),
        'posts': [p.to_dict() for p in posts]
    }

@api.route('/api/single-product/<product>')
def displayProduct(product):
    single_product = Product.query.filter_by(item_id=product).first
    print(single_product)
    return {
        'status': 'ok',
        'single product': 'nice'
    }


@api.route('/api/<item_name>', methods = ['GET', 'POST'])
def addToCart(item_name):
    data = request.json

    addedItem = Product.query.filter_by(item_name = item_name).first()
    print(addedItem)
    # if addedItem:
    current_user.saveToCart(addedItem)
    return {
        'status': 'ok',
        'message': 'added item!'
    }




@api.route('/api/cart/<string:item_name>', methods=['GET', 'POST'])
@login_required
def removeFromCart(item_name):
    print(item_name)
    deletedcart = Product.query.filter_by(item_name=item_name).first()
    # deletedcart = current_user.cart
    print(deletedcart)
    if deletedcart:
        current_user.deleteFromCart(deletedcart)

    
    return {
        'status': 'ok',
        'message': 'bye!'
    }



@api.route('/api/cart/delete-cart>', methods=['GET', 'POST'])
@login_required
def removeAllFromCart():
    
    # deletedcart = Product.query.filter_by(item_name=item_name).all() 
    ## what does each argument mean here? which is which?

    current_user.deleteAllFromCart()

    return {
        'status': 'ok',
        'message': 'all gone!'
    }

@api.route('/api/signup', methods=["POST"])
def signupAPI():
    data = request.json

    first_name = data['first_name']
    last_name = data['last_name']
    username = data['username']
    email = data['email']
    password = data['password']
            

            # add user to database
    user = User(first_name, last_name, username, email, password)

    user.saveToDB()

    return {
        'status': 'ok',
        'message': "Succesffuly created an account!"
    }


@api.route('/api/login', methods=["POST"])
@basic_auth.login_required
def getToken():
    user = basic_auth.current_user()
    return {
        'status': 'ok',
        'user': user.to_dict(),
    }
