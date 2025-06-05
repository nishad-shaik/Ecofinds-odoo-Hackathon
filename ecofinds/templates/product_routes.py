from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models import Product

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
        price = request.form['price']
        category = request.form['category']
        image = request.form['image']  # In production, use file upload handling

        product = Product(
            title=title,
            description=description,
            price=price,
            category=category,
            image=image,
            seller_id=current_user.id
        )

        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!')
        return redirect(url_for('product_bp.home'))

    return render_template('add_product.html')
