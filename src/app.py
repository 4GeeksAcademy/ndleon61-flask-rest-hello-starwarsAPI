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
from models import db, User, People, Planet, Favorite
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
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

#Gets all people
@app.route('/people', methods = ['GET'])
def get_all_people():
    people = People.query.all()
    serialized_people = [person.serialize() for person in people]
    return jsonify(serialized_people), 200

#Gets one person
@app.route('/people/<int:id>', methods = ['GET'])
def get_one_person(id):
    person = People.query.get(id)

    if person is None:
        return jsonify({"error": "Person not found"}), 404
    return jsonify(person.serialize()), 200

#Gets all planets
@app.route('/planet', methods = ['GET'])
def get_planet():
    planets = Planet.query.all()
    serialized_planets = [p.serialize() for p in planets]
    return jsonify(serialized_planets), 200


#Gets one planet
@app.route('/planet/<int:id>', methods = ['GET'])
def get_one_planet(id):
    planet = Planet.query.get(id)

    if planet is None:
        return jsonify({"error": "Unable to find planet"}), 404
    return jsonify(planet.serialize()), 200

#Gets all favorites
@app.route('/favorites', methods = ['GET'])
def get_all_favorite():
    favorites = Favorite.query.all()
    serialized_favorites = [f.serialize() for f in favorites]
    return jsonify(serialized_favorites), 200


# Gets one favorite
@app.route('/favorites/<int:id>', methods = ['GET'])
def get_one_favorite(id):
    favorite = Favorite.query.get(id)

    if favorite is None:
        return jsonify({"error": "Favorite not found"}), 404
    return jsonify(favorite.serialize()), 200

#Gets all users
@app.route('/users', methods = ['GET'])
def get_all_users():
    users = User.query.all()
    serialized_users = [user.serialize() for user in users]
    return jsonify(serialized_users), 200

#Gets one user favorite by ID
@app.route('/users/<int:user_id>/favorites', methods = ['GET'])
def get_user_favorites(user_id):
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    selialized_favorites = [f.selialize() for f in favorites]
    return jsonify(selialized_favorites), 200


#Adds a new favorite planet
@app.route('/favorite/planet/<int:planet_id>', methods = ['POST'])
def add_favorite_planet(planet_id):
    body = request.get_json()
    user_id = body.get("user_id")

    if not user_id:
        return jsonify({"error": "User not found"}), 404
    new_fav = Favorite(user_id = user_id, planet__id = planet_id, people_id = None)
    db.session.add(new_fav)
    db.session.commit()

    return jsonify(new_fav.serialize()), 201

#Adds a new favorite person
@app.route('/favorite/people/<int:people_id>', methods = ['POST'])
def add_new_person_favorite(people_id):
    body = request.get_json()
    user_id = body.get("user_id")

    if not user_id:
        return jsonify({"error": "User not found"}), 404
    
    new_fav = Favorite(user_id = user_id, planet_id = None, people_id = people_id)
    db.session.add(new_fav)
    db.session.commit()

    return jsonify(new_fav.serialize()), 201

#Deletes a favorite planet
@app.route('/favorite/planet/<int:planet_id>', methods = ['DELETE'])
def delete_favorite_planet(planet_id):
    body = request.get_json()
    user_id = body.get("user_id")

    if not user_id:
        return jsonify({"error": "User not found"}), 404
    favorite = Favorite.query.filter_by(user_id = user_id, planet_id = planet_id).first()

    if not favorite:
        return jsonify({"msg": "Favorite not found"}), 404
    
    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": "Favorite planet deleted"}), 200

#Deletes a favorite person
@app.route('/favorite/people/<int:people_id>', methods = ['DELETE'])
def delete_favorite_person(people_id):
    body = request.get_json()
    user_id = body.get("user_id")

    if not user_id:
        return jsonify({"error": "User not found"}), 404
        
    favorite = Favorite.query.filter_by(user_id = user_id, people_id = people_id).first()

    if not favorite:
        return jsonify({"error": "Favorite person not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite person deleted"}), 200