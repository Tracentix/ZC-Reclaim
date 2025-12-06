from src.core import db
from src.models.user import User

class UserRepository:
    
    def create_user(self, username, email, password_hash, role='User'):
        new_user = User(
            username=username, 
            email=email, 
            password_hash=password_hash, 
            role=role
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def get_user_by_email(self, email):
        return User.query.filter_by(email=email).first()

    def get_user_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def get_user_by_id(self, user_id):
        return User.query.get(user_id)