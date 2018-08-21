from flask import jsonify, request, Response, abort
from api.v1.views import app_views
from models import storage
import json
from models.city import City


@app_views.route('/states/<string:state_id>/cities', strict_slashes=False, methods=['GET'])
def get_states_cities(state_id):
    "returns cities with matching State id"
    s = storage.get("State", state_id)
    if not s:
        abort(404)
    else:
        return jsonify([city.to_dict() for city in s.cities])

@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_city(city_id):
    c = storage.get("City", city_id)
    if not c:
        abort(404)
    else:
        return jsonify(c.to_dict())

@app_views.route('/cities/<string:city_id>', strict_slashes=False, methods=['DELETE'])
def deletes_city(city_id):
    'deletes a city'
    a = storage.get("City", city_id)

    if not a:
        abort(404)
    else:
        storage.delete(a)
        storage.save() #not sure if i need this
        return jsonify({}), 200

@app_views.route('/states/<state_id>/cities', strict_slashes=False, methods=['POST'])
def post_a_city(state_id):
    "post a new city"
    kwargs = request.get_json()
    state = storage.get("State", state_id)

    if not state:
        abort(404)

    if not kwargs:
        abort(400, 'Not a JSON')

    if 'name' not in kwargs:
        #abort(Response('Missing name'))
        abort(400, 'Missing name')
        
    
    kwargs['state_id'] = state_id #overwrites or adds w/ valid state_id in case they provide in post

    new_city = City(**kwargs)
    storage.new(new_city)
    storage.save()

    return jsonify(new_city.to_dict()), 201

@app_views.route('cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_a_city(city_id):
    ''' update city'''
    city = storage.get("City", city_id)
    if not city:
        abort(404)

    new = request.get_json()
    if not new:
        abort(400, 'Not a JSON')
    
    for key, valuve in new.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    
    storage.save()

    return jsonify(city.to_dict()), 200

