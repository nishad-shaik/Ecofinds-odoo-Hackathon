# from flask import Flask, render_template, request, redirect, session, url_for
# from flask_login import LoginManager, login_required
# from werkzeug.security import generate_password_hash, check_password_hash
# from werkzeug.utils import secure_filename
# import os

# from models import db, User, Product, CartItem

# app = Flask(__name__)
# app.jinja_env.cache = {}

# app.secret_key = 'supersecretkey'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecofinds.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# UPLOAD_FOLDER = os.path.join('static', 'uploads')
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# db.init_app(app)

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


# @app.route('/')
# def landing():
#     query = request.args.get('q')
#     category = request.args.get('category')
#     products = Product.query
#     if query:
#         products = products.filter(Product.title.contains(query))
#     if category:
#         products = products.filter_by(category=category)
#     return render_template('landing.html', products=products.all())

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = generate_password_hash(request.form['password'])
#         user = User(username=username, email=email, password=password)
#         db.session.add(user)
#         db.session.commit()
#         return redirect('/login')
#     return render_template('register.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         user = User.query.filter_by(username=request.form['username']).first()
#         if user and check_password_hash(user.password, request.form['password']):
#             session['user_id'] = user.id
#             return redirect('/')
#     return render_template('login.html')

# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     return redirect('/')

# @app.route('/add', methods=['GET', 'POST'])
# def add_product():
#     if 'user_id' not in session:
#         return redirect('/login')
#     if request.method == 'POST':
#         title = request.form['title']
#         description = request.form['description']
#         category = request.form['category']
#         price = float(request.form['price'])
#         location = request.form['location']
#         image_file = request.files['image']
#         filename = secure_filename(image_file.filename)
#         image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         product = Product(title=title, description=description, category=category,
#                           price=price, location=location, image=filename, owner_id=session['user_id'])
#         db.session.add(product)
#         db.session.commit()
#         return redirect('/')
#     return render_template('add_product.html')

# @app.route('/product/<int:product_id>')
# def product_page(product_id):
#     product = Product.query.get_or_404(product_id)
#     return render_template('product_page.html', product=product)

# @app.route('/profile')
# def profile():
#     print(">>> PROFILE ROUTE CALLED")  # 👈 Add this
#     if 'user_id' not in session:
#         return redirect('/login')
#     user = User.query.get(session['user_id'])
#     user_products = Product.query.filter_by(owner_id=user.id).all()
#     return render_template('profile.html', user=user, user_products=user_products)


# @app.route('/edit_profile', methods=['POST'])
# def edit_profile():
#     if 'user_id' not in session:
#         return redirect('/login')
    
#     user = User.query.get(session['user_id'])
#     user.username = request.form['username']
#     user.email = request.form['email']
#     db.session.commit()

#     return redirect('/profile')


# @app.route('/cart')
# def cart():
#     if 'user_id' not in session:
#         return redirect('/login')
#     items = CartItem.query.filter_by(user_id=session['user_id']).all()
#     return render_template('cart.html', items=items)

# @app.route('/cart/add/<int:product_id>')
# def add_to_cart(product_id):
#     if 'user_id' not in session:
#         return redirect('/login')
#     cart_item = CartItem(user_id=session['user_id'], product_id=product_id)
#     db.session.add(cart_item)
#     db.session.commit()
#     return redirect('/cart')

# @app.route('/cart/remove/<int:item_id>')
# def remove_from_cart(item_id):
#     item = CartItem.query.get(item_id)
#     db.session.delete(item)
#     db.session.commit()
#     return redirect('/cart')

# @app.route('/buy/<int:product_id>')
# def buy_now(product_id):
#     if 'user_id' not in session:
#         return redirect('/login')
    
#     product = Product.query.get_or_404(product_id)
#     return render_template('buy_now.html', product=product)

# @app.route('/delete_product/<int:product_id>', methods=['POST'])
# def delete_product(product_id):
#     if 'user_id' not in session:
#         return redirect('/login')
    
#     product = Product.query.get_or_404(product_id)
    
#     if product.owner_id != session['user_id']:
#         return "Unauthorized", 403

#     image_path = os.path.join(app.config['UPLOAD_FOLDER'], product.image)
#     if os.path.exists(image_path):
#         os.remove(image_path)

#     db.session.delete(product)
#     db.session.commit()
#     return redirect('/profile')


# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Product, CartItem
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        new_user = User(
            name=name,
            username=username,
            email=email,
            phone=phone,
            password=hashed_password,
            created_at=datetime.now()
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    user = current_user
    products = Product.query.filter_by(user_id=user.id).all()
    return render_template('profile.html', user=user, products=products)

@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    user = current_user
    user.name = request.form['name']
    user.username = request.form['username']
    user.email = request.form['email']
    user.phone = request.form['phone']
    db.session.commit()
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile'))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        description = request.form.get('description', '')
        file = request.files.get('image')
        filename = None
        if file and file.filename:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        product = Product(
            name=name,
            price=price,
            description=description,
            image_filename=filename,
            owner=current_user
        )
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('profile'))
    return render_template('add.html')

@app.route('/cart')
@login_required
def cart():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    return render_template('cart.html', items=items)

@app.route('/add_to_cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    item = CartItem(user_id=current_user.id, product_id=product_id)
    db.session.add(item)
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    item = CartItem.query.get(item_id)
    if item and item.user_id == current_user.id:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for('cart'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
