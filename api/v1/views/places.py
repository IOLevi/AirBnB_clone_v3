#!/usr/bin/python3
"Places module"
from flask import jsonify, request, Response, abort
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route('cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def get_all_places(city_id):
    ''' gets all places in a city '''
    city = storage.get("City", city_id)
    if not city:
        abort(404)

    return jsonify([place.to_dict() for place in city.places]), 200


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def get_place(place_id):
    "Gets a place by place id"
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    ''' deletes places'''
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def post_place(city_id):
    '''posts a new place to city'''
    kwargs = request.get_json()
    city = storage.get("City", city_id)

    if not city:
        abort(404)

    if not kwargs:
        abort(400, 'Not a JSON')
    if 'user_id' not in kwargs:
        abort(400, 'Missing user_id')
    if 'name' not in kwargs:
        abort(400, 'Missing name')
    user = storage.get("User", kwargs['user_id'])

    if not user:
        abort(404)

    # overwrites or adds w/ valid state_id in case they provide in post
    kwargs['city_id'] = city_id

    new_place = Place(**kwargs)
    storage.new(new_place)
    storage.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    ''' updates place '''
    params = request.get_json()
    if not params:
        abort(400, 'Not a JSON')
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    for k, v in params.items():
        if k not in ['id', 'user_id', 'city_id', 'create_at', 'updated_at']:
            setattr(place, k, v)
    storage.save()
    return jsonify(place.to_dict()), 200
