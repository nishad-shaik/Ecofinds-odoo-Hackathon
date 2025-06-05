from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models import Product, Auction, User
from datetime import datetime

auction_bp = Blueprint('auction_bp', __name__)

@auction_bp.route('/auction/create/<int:product_id>', methods=['GET', 'POST'])
@login_required
def create_auction(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        min_bid = float(request.form['min_bid'])
        reserve_price = float(request.form['reserve_price'])
        end_time = datetime.strptime(request.form['end_time'], '%Y-%m-%d %H:%M')

        auction = Auction(
            product_id=product.id,
            min_bid=min_bid,
            reserve_price=reserve_price,
            end_time=end_time
        )
        product.is_auction = True
        db.session.add(auction)
        db.session.commit()
        flash('Auction created successfully!')
        return redirect(url_for('product_bp.home'))

    return render_template('create_auction.html', product=product)

@auction_bp.route('/auction/<int:auction_id>', methods=['GET', 'POST'])
def view_auction(auction_id):
    auction = Auction.query.get_or_404(auction_id)
    product = auction.product

    if request.method == 'POST':
        bid_amount = float(request.form['bid'])
        if bid_amount > auction.current_bid:
            auction.current_bid = bid_amount
            auction.highest_bidder_id = current_user.id
            db.session.commit()
            flash('Bid placed successfully!')
        else:
            flash('Bid must be higher than current bid.')

    return render_template('auction_detail.html', auction=auction, product=product)
