from flask import Blueprint, render_template, redirect, url_for, flash
from src.models.claim import Claim
from src.models.item import Item
from src.core import db, admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    pending_claims = Claim.query.filter_by(status='Pending').all()
    return render_template('admin/dashboard.html', claims=pending_claims)

@admin_bp.route('/approve/<int:claim_id>', methods=['POST'])
@admin_required
def approve_claim(claim_id):
    claim = Claim.query.get_or_404(claim_id)
    item = Item.query.get(claim.item_id)
    
    claim.status = 'Approved'
    item.status = 'Claimed' 
    
    db.session.commit()
    flash('Claim Approved.', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/reject/<int:claim_id>', methods=['POST'])
@admin_required
def reject_claim(claim_id):
    claim = Claim.query.get_or_404(claim_id)
    
    claim.status = 'Rejected'
    
    db.session.commit()
    flash('Claim Rejected.', 'info')
    return redirect(url_for('admin.dashboard'))