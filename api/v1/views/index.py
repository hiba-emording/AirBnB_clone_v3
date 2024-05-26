#!/usr/bin/python3
"""defines a route for an API endpoint"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def get_status():
    """Endpoint to get the status of the API"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'])
def get_stats():
    """Endpoint to get number of each obj by type"""
    objects_count = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(objects_count)
