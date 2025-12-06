from src.core import db
from datetime import datetime

class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)    
    type = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), default='Active')
    location = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Item {self.title}>'