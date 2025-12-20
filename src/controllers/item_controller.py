from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from src.repositories.item_repository import ItemRepository
from werkzeug.utils import secure_filename
from datetime import datetime
import os

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'src', 'static', 'uploads')

item_bp = Blueprint('item', __name__, url_prefix='/items')
item_repo = ItemRepository()

@item_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
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