from flask import Flask, request, render_template, jsonify
from flask_restful import Resource, Api
import sqlalchemy as db
#from app.data.orm.products import Product
#from app.data.orm import db_session
import random


app = Flask(__name__)
api = Api(app)

@app.route('/', methods=['GET', 'POST'])
def main():
    print(1)
    return "12231"

class Host(Resource):
    def __init__(self):
        self.count = 0
        self.sec_inv = 2

    def get(self):
        print('get')
        # visible(un sec)

        # open db
        with open('db.txt', 'r') as db:
            data = list(map(int, db.read().split()))

        new_koeff = int(data[-1])
        # request sec_inv from db
        self.count+=1
        self.sec_inv += new_koeff
        sign = random.randrange(-10, 10)
        third_num = self.sec_inv + sign

        for_sending = {"data": []}
        for_sending["data"].append({'type': 'visible', 'third_num': third_num})

        return jsonify(for_sending)

    def post(self):
        print("post")
        # invisible(5 sec)
        # maybe it shoud be in get but than it'll be kurfuffle
        task_data = request.get_json()  # {"type": "invisible"}
        if not task_data:
            return jsonify({'message': 'No data provided'})

        type = task_data.get("type")
        with open('purchase.txt', 'r') as f:
            fail = list(map(int, f.read().split()))

        k = fail[self.count] / 10
        self.count += 1

        # open db, write here k
        with open('db.txt', 'a') as db:
            db.write(k + '\n')

        for_sending = {"data": []}
        for_sending["data"].append({'type': 'invisible', 'respond': k})

        print("!!!")
        return jsonify(for_sending)  # would it work? YES


api.add_resource(Host, '/host')


if __name__ == '__main__':
    app.run(debug=True)