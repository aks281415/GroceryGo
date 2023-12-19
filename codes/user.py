from flask import redirect, url_for, request, flash, render_template
from flask_login import login_required, current_user, logout_user, login_user , LoginManager
from app import db, app, login_manager
from form import SignUpForm, LoginForm
from model import User
from model import Cart , Section , Product
from datetime import datetime




@app.route("/user")
@login_required
def user():
    if current_user.is_authenticated and not current_user.is_admin:
        return render_template('user_home.html')
    else:
        return redirect(url_for('user_login'))
    
@app.route('/user/signup', methods=["POST", "GET"])
def user_signup():
    form  = SignUpForm()
    if form.validate_on_submit():
        # first_user = User.query.first()
        # is_admin = False
        # if not first_user:
        #     is_admin = True

        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user_login'))
    return render_template('user_signup.html', form=form)

@app.route("/user/login", methods=["GET", "POST"])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return(redirect(url_for("user")))

    return render_template("user_login.html", form=form, title="Log In")

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    if current_user.is_authenticated:
        user_id = current_user.id
        quantity = int(request.form.get('quantity', 1))

       
        product = Product.query.get_or_404(product_id)

        if product.units <= 0:
            flash('Product is out of stock. Cannot add to cart.', 'error')
        else:
            if quantity > product.units:
                flash('Quantity exceeds available units. Adding maximum available units to cart.', 'warning')
                quantity = product.units

            cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
            if cart_item:
                cart_item.quantity += quantity
            else:
                cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
                db.session.add(cart_item)

           
            product.units -= quantity
            db.session.commit()

            flash('Product added to cart successfully.', 'success')


    
    return redirect(url_for('view_cart', section_id=product.section_id))




@app.route('/user/view_products/<int:section_id>')
@login_required
def user_view_products(section_id):
    section = Section.query.get_or_404(section_id)
    products = Product.query.filter_by(section_id=section_id).all()
    return render_template('user_view_products.html', section=section, products=products)

@app.route('/user/sections')
def user_sections():
    sections = Section.query.all()
    return render_template('user_sections.html', sections=sections)



@app.route('/view_cart')
@login_required
def view_cart():
    user_id = current_user.id
    cart_items = Cart.query.filter_by(user_id=user_id).all()

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render_template('view_cart.html', cart_items=cart_items, total_price=total_price)


@app.route('/delete_cart_item/<int:cart_item_id>', methods=['POST', 'DELETE'])
@login_required
def delete_cart_item(cart_item_id):
    cart_item = Cart.query.get_or_404(cart_item_id)

    if cart_item.user_id != current_user.id:
        return redirect(url_for('view_cart'))

    product = Product.query.get_or_404(cart_item.product_id)

    product.units += cart_item.quantity

    db.session.delete(cart_item)
    db.session.commit()

    return redirect(url_for('view_cart'))


@app.route('/user/search_products', methods=['GET'])
@login_required
def user_search_products():
    search_query = request.args.get('search_query')
    if search_query:
        products = Product.query.filter(
            (Product.section.has(name=search_query)) | (Product.name.contains(search_query))
        ).all()
    else:
        products = Product.query.all()

    return render_template('user_search_products.html', products=products, search_query=search_query)


@app.route('/user/logout')
def user_logout():
    logout_user()
    return redirect(url_for('home'))




@app.route('/order_placed')
def order_placed():
    return render_template('order_placement.html')






