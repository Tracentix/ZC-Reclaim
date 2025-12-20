from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from src.models.claim import Claim
from src.core import db

claim_bp = Blueprint('claim', __name__, url_prefix='/claims')

@claim_bp.route('/submit/<int:item_id>', methods=['GET', 'POST'])
def submit_claim(item_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        details = request.form.get('verification_details')
        
        new_claim = Claim(
            user_id=session['user_id'],
            item_id=item_id,
            verification_details=details
        )
        db.session.add(new_claim)
        db.session.commit()
        
        flash('Claim submitted! Waiting for Admin approval.', 'success')
        return redirect(url_for('item.dashboard'))
        
    return render_template('claim/submit_claim.html', item_id=item_id)