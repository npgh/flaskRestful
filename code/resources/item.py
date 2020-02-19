from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
# import sqlite3
from models.item import ItemModel


class Item(Resource):
    TABLE_NAME = 'items'

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every items needs a store id."
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        data = Item.parser.parse_args()
        name = data['name']
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400



        item = ItemModel(name,data['price'],data['store_id'])

        #
        item.save_to_db()
        # try:
        #     item.insert()
        # except:
        #     return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201


    @jwt_required()
    def delete(self, name):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "DELETE FROM {table} WHERE name=?".format(table=self.TABLE_NAME)
        # cursor.execute(query, (name,))
        #
        # connection.commit()
        # connection.close()
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'}
        else:
            return {'message': 'Item not found'}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        name = data['name']
        item = ItemModel.find_by_name(name)
        # updated_item = ItemModel(name,data['price'])

        if item is None:
            item = ItemModel(name,data['price'],data['store_id'])
            #item = ItemModel(name,data['price'],data['store_id']) #can be simplified to **data
            # try:
            #     updated_item.insert()
            # except:
            #     return {"message": "An error occurred inserting the item."}, 500
        else:
            item.price = data['price']
        item.save_to_db()
            # try:
            #     updated_item.update()
            # except:
            #     return {"message": "An error occurred updating the item."}, 500
        return item.json()



class ItemList(Resource):
    TABLE_NAME = 'items'

    @jwt_required()
    def get(self):
        # return {'items':[item.json() for item in ItemModel.query.all()]}
        return {'items':list(map(lambda x: x.json(),ItemModel.query.all()))}

        # items = []
        # for item in ItemModel.query:
        #     items.append({'id':item.id, 'name':item.name, 'price':item.price})
        # return {'items': items}

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM {table}".format(table=self.TABLE_NAME)
        # result = cursor.execute(query)
        # items = []
        # for row in result:
        #     items.append({'id': row[0],'name': row[1], 'price': row[2]})
        # connection.close()
        #
        # return {'items': items}
