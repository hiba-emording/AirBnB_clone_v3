#!/usr/bin/python3
"""defines a route for an API endpoint to get the status"""

from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status', methods=['GET'])
def get_status():
    """Endpoint to get the status of the API"""
    return jsonify({"status": "OK"})
