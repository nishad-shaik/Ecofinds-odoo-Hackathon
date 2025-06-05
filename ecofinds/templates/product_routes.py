from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Product, CartItem, WatchlistItem

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/')
def home():
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('homepage.html', products=products)

@product_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@product_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = float(request.form['price'])
        category = request.form['category']
        image = request.files['image']

        filename = image.filename
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

@product_bp.route('/search')
def search():
    query = request.args.get('q', '').strip()

    if query:
        products = Product.query.filter(Product.title.ilike(f'%{query}%')).all()
    else:
        products = []

    return render_template('search_results.html', products=products, query=query)

@product_bp.route('/buy/<int:product_id>', methods=['POST'])
@login_required
def buy_now(product_id):
    flash("Buy Now clicked!")
    return redirect(url_for('product_bp.product_detail', product_id=product_id))

@product_bp.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    existing_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if not existing_item:
        new_item = CartItem(user_id=current_user.id, product_id=product_id)
        db.session.add(new_item)
        db.session.commit()
        flash('Added to cart!')
    else:
        flash('Item already in cart.')
    
    return redirect(url_for('product_bp.view_cart'))


@product_bp.route('/cart')
@login_required
def view_cart():
    cart_entries = CartItem.query.filter_by(user_id=current_user.id).all()
    cart_items = [entry.product for entry in cart_entries]
    return render_template('cart_page.html', cart_items=cart_items)

@product_bp.route('/cart/remove/<int:product_id>', methods=['POST'])
@login_required
def remove_from_cart(product_id):
    item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        flash('Removed from cart.')
    return redirect(url_for('product_bp.view_cart'))

@product_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash('Checkout successful!')
    return redirect(url_for('product_bp.home'))

@product_bp.route('/wishlist')
@login_required
def view_watchlist():
    watchlist_entries = WatchlistItem.query.filter_by(user_id=current_user.id).all()
    watchlist_items = [entry.product for entry in watchlist_entries]
    return render_template('wishlist_page.html', watchlist_items=watchlist_items)

@product_bp.route('/wishlist/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_watchlist(product_id):
    existing = WatchlistItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if not existing:
        new_item = WatchlistItem(user_id=current_user.id, product_id=product_id)
        db.session.add(new_item)
        db.session.commit()
        flash("Added to wishlist!")
    else:
        flash("Item already in wishlist.")
    return redirect(url_for('product_bp.product_detail', product_id=product_id))

@product_bp.route('/wishlist/remove/<int:product_id>', methods=['POST'])
@login_required
def remove_from_watchlist(product_id):
    item = WatchlistItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        flash("Removed from wishlist.")
    return redirect(url_for('product_bp.view_watchlist'))

@product_bp.route('/profile')
@login_required
def profile():
    user = current_user
    listings = Product.query.filter_by(seller_id=user.id).order_by(Product.created_at.desc()).all()
    return render_template('profile_page.html', user=user, listings=listings)

