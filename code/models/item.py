# import sqlite3
from db import db

class ItemModel(db.Model):
    TABLE_NAME = 'items'

    __tablename__ = "items"
    #__table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision = 2))
    store = db.relationship('StoreModel')
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))


    def __init__(self,name,price,store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {"name" : self.name, "price" : self.price, "store_id" : self.store_id}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name = name).first()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM {table} WHERE name=?".format(table=cls.TABLE_NAME)
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()
        #
        # if row:
        #     return cls(*row)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "INSERT INTO {table} VALUES(?, ?)".format(table=ItemModel.TABLE_NAME)
        # cursor.execute(query, (self.name, self.price))
        #
        # connection.commit()
        # connection.close()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    # def update(self):
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()
    #
    #     query = "UPDATE {table} SET price=? WHERE name=?".format(table=cls.TABLE_NAME)
    #     cursor.execute(query, (self.price, self.name))
    #
    #     connection.commit()
    #     connection.close()
