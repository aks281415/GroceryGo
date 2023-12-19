from flask import render_template, session, request, redirect, url_for, flash 
from flask_login import login_required, current_user, logout_user, login_user
from app import app, db
from form import SignUpForm, LoginForm 
from model import Section , Product , User , Cart
from datetime import datetime



@app.route("/admin")
def admin():
    if current_user.is_authenticated and current_user.is_admin:
        return render_template('admin_home.html')
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for("admin"))


    return render_template("admin_login.html", form=form, title="Log In")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            is_admin=True 
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login")) 
    return render_template("admin_signup.html", form=form, title="Register")



@app.route('/add_section', methods=['GET', 'POST'])

def add_section():
    if not current_user.is_admin:
        return redirect(url_for('section_list'))

    if request.method == "GET":
        return render_template('add_section.html')
    if request.method == 'POST':
        section_name = request.form.get('section_name')
        section = Section(name=section_name)
        db.session.add(section)
        db.session.commit()
        return redirect(url_for('section_list'))

@app.route('/delete_section/<int:section_id>', methods=['POST'])
def delete_section(section_id):
    section = Section.query.get_or_404(section_id)

    
    if not current_user.is_admin:
        return redirect(url_for('section_list'))

    
    products = Product.query.filter_by(section_id=section_id).all()

    
    for product in products:
        db.session.delete(product)

    
    db.session.delete(section)
    db.session.commit()

    return redirect(url_for('section_list'))

@app.route('/edit_section/<int:section_id>', methods=['GET', 'POST'])

def edit_section(section_id):
    section = Section.query.get_or_404(section_id)

    if not current_user.is_admin:
        return redirect(url_for('section_list'))

    if request.method == 'POST':
        new_name = request.form.get('new_name')
        if new_name:
            section.name = new_name
            db.session.commit()
            return redirect(url_for('section_list'))

    return render_template('edit_section.html', section=section)


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if not current_user.is_admin:
        return redirect(url_for('user'))

    if request.method == 'POST':
        product_id = request.args.get('product_id')
        name = request.form['name']
        price = float(request.form['price'])
        exp_date_s = request.form['exp_date']
        manu_date_s = request.form['manufacture_date']
        units = request.form['units']
        section_id = int(request.form['section_id'])
        exp_date = datetime.strptime(exp_date_s, '%Y-%m-%d')
        manufacture_date = datetime.strptime(manu_date_s, '%Y-%m-%d')

        if product_id:
            product = Product.query.get(product_id)
            if product:
                product.name = name
                product.price = price
                product.exp_date = exp_date
                product.units = units
                product.section_id = section_id
                product.manufacture_date = manufacture_date
            else:
                return redirect(url_for('product_list'))
        else:
            product = Product(name=name, price=price, exp_date=exp_date, units=units, section_id=section_id, manufacture_date=manufacture_date)
            db.session.add(product)

        db.session.commit()
        return redirect(url_for('product_list'))

    sections = Section.query.all()

    return render_template('add_product.html', sections=sections)




    
@app.route('/view_product/<int:section_id>', methods=['GET'])
def view_product(section_id):
    section = Section.query.get_or_404(section_id)

    if current_user.is_admin:
        products = section.products
        return render_template('view_product.html', section=section, products=products)
    # else:
    #     flash("You are not authorized to access the admin view.", "error")
    #     return redirect(url_for('user_view_products', section_id=section_id))

@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if not current_user.is_admin:
        return redirect(url_for('user_home'))

    product = Product.query.get_or_404(product_id)

    section_id = product.section_id

    db.session.delete(product)
    db.session.commit()

    section = Section.query.get(section_id)
    if section.products:
        
        return redirect(url_for('view_product', section_id=section_id))
    else:
        
        return redirect(url_for('section_list'))

@app.route('/section_list', methods=['GET', 'POST']) 
def section_list():
    if not current_user.is_admin:
        return redirect(url_for('user'))

    sections = Section.query.all()
    return render_template('section_list.html', sections=sections)


@app.route('/product_list')
def product_list():
    if not current_user.is_admin:
        return redirect(url_for('user'))
    
    products = Product.query.all()
    return render_template('product_list.html', products=products)

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if not current_user.is_admin:
        return redirect(url_for('user_home'))

    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        manu_date_s = request.form['manufacture_date']
        exp_date_s = request.form['exp_date']
        units = int(request.form['units'])
        manufacture_date = datetime.strptime(manu_date_s, '%Y-%m-%d')
        exp_date = datetime.strptime(exp_date_s, '%Y-%m-%d')

        product.name = name
        product.price = price
        product.manufacture_date = manufacture_date
        product.exp_date = exp_date
        product.units = units

        db.session.commit()
        return redirect(url_for('view_product', section_id=product.section_id))

    return render_template('edit_product.html', product=product)





@app.route('/admin/logout')
def admin_logout():
    logout_user()
    return redirect(url_for('home'))





