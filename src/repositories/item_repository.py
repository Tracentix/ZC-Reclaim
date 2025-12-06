from src.core import db
from src.models.item import Item

class ItemRepository:
    
    def create_item(self, title, description, type, location, user_id, image_url=None):
        """Creates a new Lost/Found item post"""
        new_item = Item(
            title=title,
            description=description,
            type=type,          # 'Lost' or 'Found'
            location=location,
            user_id=user_id,
            image_url=image_url
        )
        db.session.add(new_item)
        db.session.commit()
        return new_item

    def get_all_active_items(self):
        """Get all items for the Dashboard (newest first)"""
        return Item.query.filter_by(status='Active').order_by(Item.created_at.desc()).all()

    def search_items(self, query):
        search = f"%{query}%"
        return Item.query.filter(Item.title.like(search)).all()