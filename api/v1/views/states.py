from flask import jsonify, request, Response, abort
from api.v1.views import app_views
from models import storage
import json
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_all_states():
    "returns all states"
    a = storage.all("State").values()

    return jsonify([b.to_dict() for b in a]) 

@app_views.route('/states/<string:state_id>', strict_slashes=False, methods=['GET'])
def get_a_states(state_id):
    "returns a state by id"
    a = storage.get("State", state_id)

    if not a:
        abort(404)
    else:
        return jsonify(a.to_dict())

@app_views.route('/states/<string:state_id>', strict_slashes=False, methods=['DELETE'])
def delete_a_states(state_id):
    'deletes a state'
    a = storage.get("State", state_id)

    if not a:
        abort(404)
    else:
        storage.delete(a)
        storage.save() #not sure if i need this
        return jsonify({}), 200

@app_views.route('/states', strict_slashes=False, methods=['POST'])
def post_a_state():
    "post a new state"
    a = request.get_json()

    if not a:
        abort(404)
        abort(Response('Not a JSON'))

    if 'name' not in a:
        abort(404)
        abort(Response('Missing name'))

    b = State(**a)#if this doesnt work, use json.load
    storage.new(b)
    storage.save()
    return jsonify(b.to_dict()), 201

@app_views.route('/states/<string:state_id>', strict_slashes=False, methods=['PUT'])
def update_a_state(state_id):
    "update a state with put"

    a = storage.get("State", state_id)

    if not a:
        abort(404)

    b = request.get_json()
    if not b:
        abort(404)
        abort(Response('Not a JSON'))

    for k, v in b.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(a, k, v)

    storage.save()

    return jsonify(a.to_dict()), 200
