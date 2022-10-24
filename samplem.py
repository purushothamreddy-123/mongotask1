from http import client
from itertools import product
from urllib import response
from flask import Flask, request, jsonify
from flask_json import FlaskJSON
from flask_mongoengine import MongoEngine
import json
from healthcheck import HealthCheck

app = Flask(__name__)
json = FlaskJSON(app)

health = HealthCheck()

app.config['MONGODB_SETTINGS'] = {
    'db': 'Student',
    'host': 'localhost',
    'port': 27017
}

db = MongoEngine()
db.init_app(app)

class dpr(db.Document):
    name = db.StringField()
    age = db.IntField()
    sub = db.StringField()
    def to_json(self):
        return {"name": self.name,
                "age": self.age,
                "sub" : self.sub}

@app.route("/")
def root_path():
    return("sita")

def test_movie():
  client = app.test_client()
  url ='/'
  response = client.get(url)
  assert response.get_data() == b'sita'



@app.route('/user/', methods=['GET'])
def get_user():
    contact = dpr.objects()
    if not contact:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(contact)


def test_get():
    client = app.test_client()
    url ='/user/'
    response =client.get(url)
    assert response. get_data()



@app.route('/user/', methods=['POST'])
def add_user():
    record = json.loads(request.data)
    contact = dpr(name=record['name'],
                age=record['age'],
                sub=record['sub'])
    contact.save()
    return jsonify(contact)


def test_post():
    client = app.test_client()
    url = '/user/'
    response = client.post(url)
    assert response.get_data()


@app.route('/user/<id>', methods=['PUT'])
def Update_user(id):
    record = json.loads(request.data)
    contact = dpr.objects.get_or_404(id=id)
    if not contact:
        return jsonify({'error': 'data not found'})
    else:
        contact.update(name=record['name'],
                    age=record['age'],
                    sub=record["sub"])
    return jsonify(contact)

def test_put():
    client = app.test_client()
    url = '/user/<id>'
    response = client.put(url)
    assert response.status_code==500


@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    contact = dpr.objects(id=id)
    if not contact:
        return jsonify({'error': 'data not found'})
    else:
        contact.delete()
    return jsonify(contact)

def test_delete():
    client = app.test_client()
    url = '/user/'
    response = client.get(url)
    assert response.get_data()





class car(db.Document):
    name = db.StringField()
    model = db.StringField()
    price = db.StringField()
    def to_json(self):
        return {"name": self.name,
                "model": self.model,
                "price" : self.price}



@app.route('/model/', methods=['GET'])
def get_model():
    product = car.objects()
    if not product:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(product)



@app.route('/model/', methods=['POST'])
def add_model():
    record = json.loads(request.data)
    product = car(name=record['name'],
                model=record['model'],
                price=record['price'])
    product.save()
    return jsonify(product)



@app.route('/model/<id>', methods=['PUT'])
def Update_model(id):
    record = json.loads(request.data)
    product = car.objects.get_or_404(id=id)
    if not product:
        return jsonify({'error': 'data not found'})
    else:
        product.update(name=record['name'],
                    model=record['model'],
                    price=record['price'])
        # product.save()
    return jsonify(product)


@app.route('/model/<id>', methods=['DELETE'])
def delete_model(id):
    product = car.objects(id=id)
    if not product:
        return jsonify({'error': 'data not found'})
    else:
        product.delete()
    return jsonify(product)




app.add_url_rule('/healthcheck', 'healthcheck', view_func=lambda: health.run())

if __name__ == "__main__":
    app.run(debug=True)