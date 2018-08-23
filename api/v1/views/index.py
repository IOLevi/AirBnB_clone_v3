#!/usr/bin/python3
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def get_status():
    "returns status ok, 200"
    return jsonify({'status': 'OK'}), 200


@app_views.route('/stats', strict_slashes=False)
def get_stats():
    '''add count method from storage '''
    new_dict = {}
    new_dict["amenities"] = storage.count("Amenity")
    new_dict["cities"] = storage.count("City")
    new_dict["places"] = storage.count("Place")
    new_dict["reviews"] = storage.count("Review")
    new_dict["states"] = storage.count("State")
    new_dict["users"] = storage.count("User")

    return jsonify(new_dict), 200
