from app import app
from flask import render_template, flash, url_for, redirect, request
import requests
from .models import Product
from flask_login import current_user, login_required


@app.route('/populate')
@login_required
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

            # posts = Product.query.all()

            continue
            # return render_template('home.html', posts = posts)

    posts = Product.query.all()
    print(posts)
    return render_template('home.html', posts = posts)

@app.route('/')
@login_required
def homePage():
    posts = Product.query.all()
    print(posts)
    return render_template('home.html', posts = posts)


@app.route('/all_products')
def displayAllProducts():
    
    posts = Product.query.all()
    print(posts)
    return render_template('home.html', posts = posts)

@app.route('/single-product/<product>')
def displayProduct(product):
    single_product = Product.query.filter_by(item_id=product).first
    print(single_product)
    return render_template('single_product.html', single_product=single_product)

    

@app.route('/<item_name>', methods = ['GET', 'POST'])
@login_required
def addToCart(item_name):
    addedItem = Product.query.filter_by(item_name = item_name).first()
    print(addedItem)
    # if addedItem:
    current_user.saveToCart(addedItem)


    return redirect(url_for('cart'))

@app.route('/cart', methods = ['GET', 'POST'])
@login_required
def cart():
    
    usercart= current_user.cart

    grand_total = 0
    for item in usercart:
        grand_total += item.price

    return render_template('cart.html', usercart=usercart, grand_total=grand_total)

@app.route('/cart/<string:item_name>', methods=['GET', 'POST'])
@login_required
def removeFromCart(item_name):
    print(item_name)
    deletedcart = Product.query.filter_by(item_name=item_name).first()
    # deletedcart = current_user.cart
    print(deletedcart)
    if deletedcart:
        current_user.deleteFromCart(deletedcart)

    return redirect(url_for('cart'))
    # return render_template('cart.html')


@app.route('/cart/delete-cart>', methods=['GET', 'POST'])
@login_required
def removeAllFromCart():
    
    # deletedcart = Product.query.filter_by(item_name=item_name).all() 
    ## what does each argument mean here? which is which?

    current_user.deleteAllFromCart()

    # deletedcart = current_user.cart
    # print(deletedcart)
    # if deletedcart:
    #     current_user.deleteFromCart(deletedcart) ## should we add a deleteAll function to the model? or do a for loop to retrieve all the items? how to pass multiple parameters at once without knowing exactly how many one will grab? (depends on how many items in cart)

    return redirect(url_for('cart'))