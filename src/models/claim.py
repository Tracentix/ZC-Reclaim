from src.core import db
from datetime import datetime

class Claim(db.Model):
    __tablename__ = 'claim'
    
    id = db.Column(db.Integer, primary_key=True)
    verification_details = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Pending')
    claim_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    
    user = db.relationship('User', backref='claims')
    item = db.relationship('Item', backref='claims')