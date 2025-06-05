from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from werkzeug.utils import secure_filename
import os

from app import db, login_manager
from models import User

auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']

        # Handle profile picture
        profile_pic = request.files.get('profile_picture')
        if profile_pic and profile_pic.filename != '':
            filename = secure_filename(profile_pic.filename)
            profile_pic_path = os.path.join('static/uploads', filename)
            profile_pic.save(profile_pic_path)
        else:
            filename = 'default_profile.png'  # fallback if no file uploaded

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered.')
            return redirect(url_for('auth.register'))

        hashed_pw = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password=hashed_pw,
            phone=phone,
            profile_pic=filename
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Account created! Please log in.')
        return redirect(url_for('auth.login'))

    return render_template('signup.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Please enter both username and password.")
            return redirect(url_for('auth.login'))

        user = User.query.filter_by(username=username).first()

        if not user:
            flash("User not found. Please sign up.")
            return redirect(url_for('auth.register'))

        if check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('product_bp.home'))
        else:
            flash('Invalid password.')
            return redirect(url_for('auth.login'))

    return render_template('login.html')





@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('auth.login'))
