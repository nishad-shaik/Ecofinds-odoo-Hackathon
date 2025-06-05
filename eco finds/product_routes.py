from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, Product, CartItem, WatchlistItem, User
from collections import defaultdict

product_bp = Blueprint('product_bp', __name__)

# -------------------- Home --------------------
@product_bp.route('/')
def home():
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('homepage.html', products=products)

# -------------------- All Categories Grouped --------------------
@product_bp.route('/categories')
def view_categories():
    all_products = Product.query.all()
    categories = defaultdict(list)
    for product in all_products:
        categories[product.category].append(product)
    return render_template('categories.html', categories=categories)

# -------------------- Individual Category Page --------------------
@product_bp.route('/categories/<string:category_name>')
def category_page(category_name):
    products = Product.query.filter(Product.category.ilike(category_name)).all()
    return render_template('category_page.html', category=category_name, products=products)

# -------------------- Product Detail --------------------
@product_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

# -------------------- Add Product --------------------
@product_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = float(request.form['price'])
        category = request.form['category']
        image = request.files['image']

        filename = secure_filename(image.filename)
        image.save(f'static/uploads/{filename}')

        product = Product(
            title=title,
            description=description,
            price=price,
            category=category,
            image=filename,
            seller_id=current_user.id
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!')
        return redirect(url_for('product_bp.home'))

    return render_template('add_product.html')

# -------------------- Search --------------------
@product_bp.route('/search')
def search():
    query = request.args.get('q', '').strip()
    products = Product.query.filter(Product.title.ilike(f'%{query}%')).all() if query else []
    return render_template('search_results.html', products=products, query=query)

# -------------------- Cart --------------------
@product_bp.route('/cart')
@login_required
def view_cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    return render_template('cart_page.html', cart_items=cart_items)

@product_bp.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    if not CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first():
        item = CartItem(user_id=current_user.id, product_id=product_id)
        db.session.add(item)
        db.session.commit()
        flash("Added to cart!")
    return redirect(url_for('product_bp.view_cart'))

@product_bp.route('/cart/remove/<int:product_id>', methods=['POST'])
@login_required
def remove_from_cart(product_id):
    item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        flash("Removed from cart.")
    return redirect(url_for('product_bp.view_cart'))

@product_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash("Checkout successful!")
    return redirect(url_for('product_bp.home'))

# -------------------- Wishlist --------------------
@product_bp.route('/watchlist')
@login_required
def view_watchlist():
    wishlist_items = WatchlistItem.query.filter_by(user_id=current_user.id).all()
    return render_template('wishlist_page.html', wishlist_items=wishlist_items)

@product_bp.route('/watchlist/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_watchlist(product_id):
    if not WatchlistItem.query.filter_by(user_id=current_user.id, product_id=product_id).first():
        item = WatchlistItem(user_id=current_user.id, product_id=product_id)
        db.session.add(item)
        db.session.commit()
        flash("Added to wishlist!")
    return redirect(url_for('product_bp.product_detail', product_id=product_id))

@product_bp.route('/watchlist/remove/<int:product_id>', methods=['POST'])
@login_required
def remove_from_watchlist(product_id):
    item = WatchlistItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        flash("Removed from wishlist.")
    return redirect(url_for('product_bp.view_watchlist'))

# -------------------- Buy Now --------------------
@product_bp.route('/buy/<int:product_id>', methods=['POST'])
@login_required
def buy_now(product_id):
    flash("Buy Now clicked!")
    return redirect(url_for('product_bp.product_detail', product_id=product_id))

# -------------------- Profile --------------------
@product_bp.route('/profile')
@login_required
def profile():
    user = current_user
    listings = Product.query.filter_by(seller_id=user.id).all()
    return render_template('profile_page.html', user=user, listings=listings)

@product_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = current_user

    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.phone = request.form['phone']

        if 'profile_pic' in request.files:
            pic = request.files['profile_pic']
            if pic and pic.filename != '':
                filename = secure_filename(pic.filename)
                pic.save(f'static/uploads/{filename}')
                user.profile_pic = filename

        db.session.commit()
        flash("Profile updated successfully!")
        return redirect(url_for('product_bp.profile'))

    return render_template('edit_profile.html', user=user)
