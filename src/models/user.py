from src.db import db, CommonModel


class Users(CommonModel, db.Model):
    """ Simple user class. """
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    username = db.Column('username', db.String, nullable=False)
    email = db.Column('email', db.String, nullable=False)
    password = db.Column('password', db.String(256), nullable=False)
