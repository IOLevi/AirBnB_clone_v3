from flask import jsonify, request, Response, abort
from api.v1.views import app_views
from models import storage
import json
from models.amenity import Amenity

#works
@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def get_all_amenities():
    ''' returns all the amenities'''
    allAmenities = storage.all("Amenity").values()

    return jsonify([amenity.to_dict() for amenity in allAmenities])

 #works     
@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=['GET'])
def get_amenity(amenity_id):
    ''' returns amenity based on id'''
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())

#works
@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=['DELETE'])
def delete_amenity(amenity_id):
    ''' deletes amenity based on id '''
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200

#works...i think
@app_views.route('/amenities/', strict_slashes=False, methods=['POST'])
def post_new_amenity():
    ''' creates new amenity '''
    kwargs = request.get_json()
    if not kwargs:
        abort(400)
        abort(Response('Not a JSON'))
    if 'name' not in kwargs:
        abort(400)
        abort(Response('Missing name'))
    new_amenity = Amenity(**kwargs)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201

@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=['PUT'])
def change_amenity(amenity_id):
    ''' changes value of amenity '''
    new = request.get_json()
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    if not new:
        abort(400)
        abort(Response('Not a JSON'))
    
    for key,value in new.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
