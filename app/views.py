from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, login_required, LoginManager, logout_user
from app import app, db, bcrypt
from app.models import User, Product
from app.forms import LoginForm, RegistrationForm, UpdateProfileForm, ProductForm

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/", methods=['GET', 'POST'])
@login_required
def home():
    products = Product.query.all()

    search_term = request.form.get('search_term', '')

    if search_term:
        products = Product.query.filter(Product.name.ilike(f"%{search_term}%")).all()

    return render_template("home.html", products=products, search_term=search_term)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            phone=form.phone.data,
            address=form.address.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/profile/<username>", methods=['GET', 'POST'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    form = UpdateProfileForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.phone = form.phone.data
        user.address = form.address.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile', username=user.username))
    return render_template("profile.html", user=user, form=form)


@app.route("/edit_profile/<username>", methods=['GET', 'POST'])
@login_required
def edit_profile(username):
    user = User.query.filter_by(username=username).first()
    form = UpdateProfileForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.phone = form.phone.data
        user.address = form.address.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile', username=user.username))
    return render_template("update_profile.html", form=form)


@app.route("/add_product", methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            quantity=form.quantity.data,
            price=form.price.data,
            description=form.description.data,
            ingredients=form.ingredients.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('home'))
    return render_template("add_product.html", form=form)


@app.route("/view_product/<int:product_id>", methods=['GET', 'POST'])
@login_required
def view_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        if current_user.is_authenticated:
            current_user.cart.append(product)
            db.session.commit()
            flash('Product added to your cart!', 'success')
        else:
            flash('You need to log in to add products to your cart.', 'warning')

    return render_template("view_product.html", product=product)


@app.route("/cart")
@login_required
def cart():
    user_cart_ids = [product.id for product in current_user.cart]
    if not user_cart_ids:
        flash('Your cart is empty.', 'info')
        return render_template("cart.html", products=[], total_price=0)
    
    user_cart = user_cart_ids
    products_in_cart = Product.query.filter(Product.id.in_(user_cart)).all()

    for product in products_in_cart:
        product.price_formatted = "{:,.2f}".format(product.price).replace('.', ',')

    total_price = sum(product.price for product in products_in_cart)
    total_price_formatted = "{:,.2f}".format(total_price).replace('.', ',')

    return render_template("cart.html", products=products_in_cart, total_price=total_price_formatted)


@app.route("/checkout", methods=['POST'])
@login_required
def checkout():
    flash('Compra realizada com sucesso!', 'success')
    return redirect(url_for('cart'))


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))