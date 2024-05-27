#!/usr/bin/python3
"""View for City objects that handles default RESTful API actions"""

from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_state_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = state.cities
    return jsonify([city.to_dict() for city in cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a City"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    if 'name' not in data:
        abort(400, description="Missing name")

    new_city = City(**data)
    new_city.state_id = state_id
    storage.new(new_city)
    storage.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    storage.save()

    return jsonify(city.to_dict()), 200
