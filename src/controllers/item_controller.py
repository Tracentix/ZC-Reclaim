from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from src.repositories.item_repository import ItemRepository
from src.models.item import Item 
from src.models.claim import Claim 
from src.core import db             
from werkzeug.utils import secure_filename
from datetime import datetime
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(current_dir, '..', 'static', 'uploads')

item_bp = Blueprint('item', __name__, url_prefix='/items')
item_repo = ItemRepository()

@item_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    query = request.args.get('q')
    
    if query:
        items = item_repo.search_items(query)
    else:
        items = item_repo.get_all_active_items()
        
    return render_template('item/dashboard.html', items=items, username=session.get('username'))

@item_bp.route('/report/<item_type>', methods=['GET', 'POST'])
def report(item_type):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        image_url = None
        
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                filename = secure_filename(file.filename)
                unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                
                if not os.path.exists(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)
                    
                file.save(os.path.join(UPLOAD_FOLDER, unique_filename))
                image_url = unique_filename

        item_repo.create_item(
            title=request.form.get('title'),
            description=request.form.get('description'),
            type=item_type,
            location=request.form.get('location'),
            user_id=session['user_id'],
            image_url=image_url
        )
        
        flash(f'{item_type} Item Reported Successfully!', 'success')
        return redirect(url_for('item.dashboard'))

    return render_template('item/report.html', item_type=item_type)

@item_bp.route('/my_items')
def my_items():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    
    my_reported_items = Item.query.filter_by(user_id=user_id).order_by(Item.created_at.desc()).all()
    
    my_claims = Claim.query.filter_by(user_id=user_id).order_by(Claim.claim_date.desc()).all()
    
    return render_template('item/my_items.html', items=my_reported_items, claims=my_claims)

@item_bp.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    item = Item.query.get_or_404(item_id)
    
    if item.user_id != session['user_id'] and session.get('role') != 'Admin':
        flash('You are not authorized to delete this item.', 'danger')
        return redirect(url_for('item.dashboard'))
    
    try:
        Claim.query.filter_by(item_id=item_id).delete()
        
        db.session.delete(item)
        db.session.commit()
        
        flash('Item deleted successfully.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting item: {str(e)}', 'danger')
    
    return redirect(url_for('item.my_items'))