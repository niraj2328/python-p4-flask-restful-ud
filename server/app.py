#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json_encoder.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Index(Resource):

    def get(self):
        response_dict = {
            "index": "Welcome to the Newsletter RESTful API"
        }

        return jsonify(response_dict)

api.add_resource(Index, '/')

class Newsletters(Resource):

    def get(self):
        response_dict_list = [n.to_dict() for n in Newsletter.query.all()]

        return jsonify(response_dict_list)

    def post(self):
        new_record = Newsletter(
            title=request.form['title'],
            body=request.form['body']
        )

        db.session.add(new_record)
        db.session.commit()

        response_dict = new_record.to_dict()

        return jsonify(response_dict), 201

api.add_resource(Newsletters, '/newsletters')

class NewsletterByID(Resource):

    def get(self, id):
        record = Newsletter.query.get_or_404(id)
        response_dict = record.to_dict()

        return jsonify(response_dict)

    def patch(self, id):
        record = Newsletter.query.get_or_404(id)

        for attr in request.form:
            setattr(record, attr, request.form[attr])

        db.session.commit()

        response_dict = record.to_dict()

        return jsonify(response_dict)

    def delete(self, id):
        record = Newsletter.query.get_or_404(id)

        db.session.delete(record)
        db.session.commit()

        response_dict = {"message": "record successfully deleted"}

        return jsonify(response_dict)

api.add_resource(NewsletterByID, '/newsletters/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
