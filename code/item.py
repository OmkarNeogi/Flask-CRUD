from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

import sqlite3

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * from items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item':{'name':row[0], 'price':row[1]}}
        return None
        # return {'message':'item does not exist'}, 404

    @classmethod
    def insert_item(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items values (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    @classmethod
    def update_price(cls, item):
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        cur.execute('UPDATE items SET price=? where name=?', (item['price'], item['name'],))
        con.commit()
        con.close()

        return item

    @jwt_required()
    def get(self, name):
        return self.find_by_name(name)

    def post(self, name):
        item = self.find_by_name(name)
        if item:
            return {'message':'item already exists'}, 400

        data = Item.parser.parse_args()
        item = {'name':name, 'price': data['price']}

        try:
            self.insert_item(item)
        except:
            return {'message':'There was an error inserting the item.'}, 500
        return item, 201

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = self.find_by_name(name)
        if not item:
            item = {'name':name, 'price':data['price']}
            self.insert_item(item)
            return item, 201
        else:
            item = {'name':name, 'price':data['price']}
            self.update_price(item)
            
        return item, 201

    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message':'item deleted'}


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * from items"
        response = cursor.execute(query, ())
        result = [{'name':row[0], 'price':row[1]} for row in response]

        # for row in response:
        #     result[row[0]] = row[1]

        return result