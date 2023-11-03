"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Vehicle, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def list_users():
    users = User.query.all()
    serialized_users = [user.serialize() for user in users ]
    return jsonify(serialized_users), 200

@app.route('/user/<int:id>', methods=['GET'])
def list_user(id):
    user = User.query.get(id)
    return jsonify(user.serialize()), 200

@app.route('/character', methods=['GET', 'POST'])
def handle_characters_request():

    if request.method == 'GET':
        characters = Character.query.all()
        serialized_characters = [character.serialize() for character in characters ]
        return jsonify(serialized_characters), 200
    
    if request.method == 'POST':
        data = request.get_json()

        if not data:
            return jsonify({"message": "Invalid request data"}), 400
        
        new_character = Character(
            image_url = data.get("image_url", "Unknown"),
            name = data.get("name"),
            description = data.get("description"),
            gender = data.get("gender"),
            height = data.get("height"),
            hair_color = data.get("hair_color"),
            eye_color = data.get("eye_color"),
            birth_year = data.get("birth_year")
        )

        db.session.add(new_character)
        db.session.commit()

        return jsonify({"message": "Character added successfully"}), 201

@app.route('/character/<int:character_id>', methods=['GET'])
def list_character(character_id):
    character = Character.query.get(character_id)
    return jsonify(character.serialize()), 200

@app.route('/planet', methods=['GET', 'POST'])
def handle_planets_request():

    if request.method == 'GET':

        planets = Planet.query.all()
        serialized_planets = [planet.serialize() for planet in planets ]
        return jsonify(serialized_planets), 200
    
    if request.method == 'POST':
        data = request.get_json()

        if not data:
            return jsonify({"message": "Invalid request data"}), 400
        
        new_planet = Planet(
            image_url = data.get("image_url", "Unknown"),
            name = data.get("name"),
            description = data.get("description"),
            climate = data.get("description"),
            population = data.get("population"),
            terrain = data.get("terrain"),
            diameter = data.get("diameter"),
            surface_water = data.get("surface_water"),
            orbital_period = data.get("orbital_period")
        )

        db.session.add(new_planet)
        db.session.commit()

        return jsonify({"message": "Planet added successfully"}), 201


@app.route('/planet/<int:planet_id>', methods=['GET'])
def list_planet(planet_id):
    planet = Planet.query.get(planet_id)
    return jsonify(planet.serialize()), 200

@app.route('/vehicle', methods=['GET', 'POST'])
def handle_vehicles_request():

    if request.method == 'GET':

        vehicles = Vehicle.query.all()
        serialized_vehicles = [vehicle.serialize() for vehicle in vehicles ]
        return jsonify(serialized_vehicles), 200
    
    if request.method == 'POST':
        data = request.get_json()

        if not data:
            return jsonify({"message": "Invalid request data"}), 400
        
        new_vehicle = Vehicle(
            image_url = data.get("image_url", "Unknown"),
            name = data.get("name"),
            description = data.get("description"),
            model = data.get("model"),
            manufacturer = data.get("manufacturer"),
            price = data.get("price")
        )

        db.session.add(new_vehicle)
        db.session.commit()

        return jsonify({"message": "Vehicle added successfully"}), 201

@app.route('/vehicle/<int:vehicle_id>', methods=['GET'])
def list_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    return jsonify(vehicle.serialize()), 200

@app.route('/user/favorite')
def list_user_favorites():
    user_id = 1
    favorites = Favorites.query.filter_by(user_id = user_id).all()
    serialized_favorites = [favorite.serialize() for favorite in favorites]
    return jsonify(serialized_favorites), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST', 'DELETE'])
def handle_planet_favortie(planet_id):
    user_id = 1
    planet = Planet.query.get(planet_id)

    if not planet:
        return jsonify({"message": "Planet not fount"}), 404
    
    if request.method == 'POST':
    
        favorite = Favorites(user_id=user_id, planet_id=planet.id, character_id=None, vehicle_id=None)
        db.session.add(favorite)
        db.session.commit()

        return jsonify({"message": "Planet added to favorites"}), 201
    
    if request.method == 'DELETE':

        favorite = Favorites.query.filter_by(user_id=user_id, planet_id = planet.id).first()

        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "Planet removed from favorites"}), 200


@app.route('/favorite/character/<int:character_id>', methods=['POST', 'DELETE'])
def handle_character_favortie(character_id):
    user_id = 1
    character = Character.query.get(character_id)

    if not character:
        return jsonify({"message": "Character not fount"}), 404
    
    if request.method == 'POST':
    
        favorite = Favorites(user_id=user_id, planet_id=None, character_id=character.id, vehicle_id=None)
        db.session.add(favorite)
        db.session.commit()

        return jsonify({"message": "Character added to favorites"}), 201
    
    if request.method == 'DELETE':

        favorite = Favorites.query.filter_by(user_id=user_id, character_id = character.id).first()

        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "Character removed from favorites"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
