from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from src.repositories.user_repository import UserRepository
from sqlalchemy.exc import IntegrityError 

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
user_repo = UserRepository()

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if user_repo.get_user_by_email(email):
            flash('Email address already registered!', 'danger')
            return redirect(url_for('auth.register'))
        
        try:
            hashed_pw = generate_password_hash(password)
            user_repo.create_user(username, email, hashed_pw)
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        
        except IntegrityError:
            flash('Username is already taken.', 'danger')
            return redirect(url_for('auth.register'))
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = user_repo.get_user_by_email(email)

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('item.dashboard'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))