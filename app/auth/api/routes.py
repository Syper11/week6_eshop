from flask import Blueprint, request
import requests
from ...models import Product, User
from ..apiauthhelper import basic_auth_required, token_auth_required, basic_auth, token_auth
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
    
@api.post('/api/cart/add')
@token_auth.login_required
def addToCartAPI():
    data = request.json
    user = token_auth.current_user()

    product_id = data['productId']
    product = Product.query.get(product_id)

    
    user.saveToCart(product)

    return{
        'status': 'ok',
        'message': f'Succesfully added "{product.item_name}"'
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

@api.get('/api/cart/get')
@token_auth.login_required
def getCartAPI():
    user = token_auth.current_user()
    cart = [Product.query.get(c.product.id).to_dict() for c in user.cart]
    
    return {
        'status': 'ok',
        'cart': cart
    }

@api.post('/api/cart/remove')
@token_auth.login_required
def removeFromCartAPI():
    data = request.json
    user = token_auth.current_user()

    product_id = data['productId']
    

    c = User.query.filter_by(user_id=user.id).filter_by(product_id=product_id).first()
    print(c)
    c.deleteFromCartt(product_id)
    
    return {
        'status': 'ok',
        'message': 'Succesfully removed item from cart!'
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
