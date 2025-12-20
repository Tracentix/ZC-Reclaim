from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flask import session, flash, redirect, url_for

db = SQLAlchemy()

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'Admin':
            flash('Access denied. Admins only.', 'danger')
            return redirect(url_for('item.dashboard'))
        return f(*args, **kwargs)
    return decorated_function