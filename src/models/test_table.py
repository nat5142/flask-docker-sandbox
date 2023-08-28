from src.db import db, CommonModel


class TestTable(CommonModel, db.Model):
    __tablename__ = 'test_table'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    stringfield1 = db.Column('stringfield1', db.String)
    stringfield2 = db.Column('stringfield2', db.String)
    integerfield1 = db.Column('integerfield1', db.String)
    integerfield2 = db.Column('integerfield2', db.String)
