from db import db

class StoreModel(db.Model):
    TABLE_NAME = 'stores'

    __tablename__ = "stores"
    #__table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel',lazy='dynamic')    #,lazy='dynamic'

    def __init__(self,name):
        self.name = name

    def json(self):
        return {"name" : self.name, "items" : [item.json() for item in self.items.all()]} #add all if lazy=dynamic
        #once we add "lazy=dynamic" self."store_id":id ,items becomes query builder and we can use all() method on it.

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name = name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
