from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Spoiler Class/Model
class Spoiler(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), unique=True)
  description = db.Column(db.String(1000))
  cover = db.Column(db.String(200))
  genres = db.Column(db.String(100))

  def __init__(self, title, description, cover, genres):
    self.title = title
    self.description = description
    self.cover = cover
    self.genres = genres

# Spoiler Schema
class SpoilerSchema(ma.Schema):
  class Meta:
    fields = ('id', 'title', 'description', 'cover', 'genres')

# Init schema
spoiler_schema = SpoilerSchema()
spoilers_schema = SpoilerSchema(many=True)

# Create a Spoiler
@app.route('/spoiler', methods=['POST'])
def add_spoiler():
  title = request.json['title']
  description = request.json['description']
  cover = request.json['cover']
  genres = request.json['genres']

  new_spoiler = Spoiler(title, description, cover, genres)

  db.session.add(new_spoiler)
  db.session.commit()

  return spoiler_schema.jsonify(new_spoiler)

# Get All Spoilers
@app.route('/spoiler', methods=['GET'])
def get_spoilers():
  all_spoilers = Spoiler.query.all()
  result = spoilers_schema.dump(all_spoilers)
  return jsonify(result)

# Get Single Spoilers
@app.route('/spoiler/<id>', methods=['GET'])
def get_spoiler(id):
  spoiler = Spoiler.query.get(id)
  return spoiler_schema.jsonify(spoiler)

# Update a Spoiler
@app.route('/spoiler/<id>', methods=['PUT'])
def update_spoiler(id):
  spoiler = Spoiler.query.get(id)

  title = request.json['title']
  description = request.json['description']
  cover = request.json['cover']
  genres = request.json['genres']

  spoiler.title = title
  spoiler.description = description
  spoiler.cover = cover
  spoiler.genres = genres

  db.session.commit()

  return spoiler_schema.jsonify(spoiler)

# Delete Spoiler
@app.route('/spoiler/<id>', methods=['DELETE'])
def delete_spoiler(id):
  spoiler = Spoiler.query.get(id)
  db.session.delete(spoiler)
  db.session.commit()

  return spoiler_schema.jsonify(spoiler)

# Run Server
if __name__ == '__main__':
  app.run(debug=True)