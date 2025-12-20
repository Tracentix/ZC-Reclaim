from src.core import db
from src.models.item import Item

class ItemRepository:
    
    def create_item(self, title, description, type, location, user_id, image_url=None):
        new_item = Item(
            title=title,
            description=description,
            type=type,
            location=location,
            user_id=user_id,
            image_url=image_url,
            status='Active'
        )
        db.session.add(new_item)
        db.session.commit()
        return new_item

    def get_all_active_items(self):
        return Item.query.filter_by(status='Active').order_by(Item.created_at.desc()).all()

    def search_items(self, query):
        return Item.query.filter(Item.title.ilike(f'%{query}%')).filter_by(status='Active').all()