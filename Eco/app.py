from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os


from models import db, User, Product, CartItem


app = Flask(__name__)
app.jinja_env.cache = {}

app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecofinds.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists('static/uploads'):
    os.makedirs('static/uploads')

db.init_app(app)

@app.route('/')
def landing():
    query = request.args.get('q')
    category = request.args.get('category')
    products = Product.query
    if query:
        products = products.filter(Product.title.contains(query))
    if category:
        products = products.filter_by(category=category)
    return render_template('landing.html', products=products.all())

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            return redirect('/')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if 'user_id' not in session:
        return redirect('/login')
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        price = float(request.form['price'])
        location = request.form['location']
        image_file = request.files['image']
        filename = secure_filename(image_file.filename)
        image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        product = Product(title=title, description=description, category=category,
                          price=price, location=location, image=filename, owner_id=session['user_id'])
        db.session.add(product)
        db.session.commit()
        return redirect('/')
    return render_template('add_product.html')

@app.route('/product/<int:product_id>')
def product_page(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_page.html', product=product)

@app.route('/profile')
def profile():
    print(">>> PROFILE ROUTE CALLED")  # 👈 Add this
    if 'user_id' not in session:
        return redirect('/login')
    user = User.query.get(session['user_id'])
    user_products = Product.query.filter_by(owner_id=user.id).all()
    return render_template('profile.html', user=user, user_products=user_products)


@app.route('/edit_profile', methods=['POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect('/login')
    
    user = User.query.get(session['user_id'])
    user.username = request.form['username']
    user.email = request.form['email']
    db.session.commit()

    return redirect('/profile')


@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect('/login')
    items = CartItem.query.filter_by(user_id=session['user_id']).all()
    return render_template('cart.html', items=items)

@app.route('/cart/add/<int:product_id>')
def add_to_cart(product_id):
    if 'user_id' not in session:
        return redirect('/login')
    cart_item = CartItem(user_id=session['user_id'], product_id=product_id)
    db.session.add(cart_item)
    db.session.commit()
    return redirect('/cart')

@app.route('/cart/remove/<int:item_id>')
def remove_from_cart(item_id):
    item = CartItem.query.get(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect('/cart')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

