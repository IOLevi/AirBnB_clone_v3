#!/usr/bin/python3
"Users module"
from flask import jsonify, request, Response, abort
from api.v1.views import app_views
from models import storage
import json
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_all_users():
    ''' gets all users and returns'''
    return jsonify([user.to_dict() for user in storage.all("User").values()])


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_user(user_id):
    ''' gets user based on id '''
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    ''' deletes user based on id '''
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 201


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def new_user():
    ''' posts a new user '''
    kwargs = request.get_json()
    if not kwargs:
        abort(400, "Not a JSON")
    if 'email' not in kwargs:
        abort(400, 'Missing email')
    if 'password' not in kwargs:
        abort(400, 'Missing password')

    new_user = User(**kwargs)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def change_user(user_id):
    ''' changes value of current user'''
    user = storage.get("User", user_id)
    param = request.get_json()
    if not user:
        abort(404)
    if not param:
        abort(400, 'Not a JSON')
    for key, value in param.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)

    storage.save()
    return jsonify(user.to_dict()), 200
