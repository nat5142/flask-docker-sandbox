from werkzeug.security import generate_password_hash, check_password_hash

from src.db import db, CommonModel


class Users(CommonModel, db.Model):
    """ Simple user class. """
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    username = db.Column('username', db.String, nullable=False)
    email = db.Column('email', db.String, nullable=False)
    password_hash = db.Column('password_hash', db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
