#!/usr/bin/python3
from flask import jsonify, request, Response, abort
from api.v1.views import app_views
from models import storage
import json
from models.review import Review


@app_views.route(
    '/places/<place_id>/reviews',
    strict_slashes=False,
    methods=['GET'])
def get_all_reviews(place_id):
    ''' gets all reviews of place '''
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def get_review(review_id):
    ''' get review based on id'''
    rev = storage.get("Review", review_id)
    if not rev:
        abort(404)
    return jsonify(rev.to_dict())


@app_views.route(
    '/reviews/<review_id>',
    strict_slashes=False,
    methods=['DELETE'])
def delete_review(review_id):
    ''' delete review based on id'''
    rev = storage.get("Review", review_id)
    if not rev:
        abort(404)
    storage.delete(rev)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/places/<place_id>/reviews',
    strict_slashes=False,
    methods=['POST'])
def post_review(place_id):
    ''' post new review'''
    place = storage.get("Place", place_id)
    kwargs = request.get_json()
    if not place:
        abort(404)
    if not kwargs:
        abort(400, 'Not a JSON')
    if 'user_id' not in kwargs:
        abort(400, 'Missing user_id')
    if 'text' not in kwargs:
        abort(400, 'Missing text')
    user = storage.get("User", user_id)
    if not user:
        abort(404)

    new_review = Review(**kwargs)
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    ''' update review '''
    rev = storage.get("Review", review_id)
    if not rev:
        abort(404)
    params = request.get_json()
    if not params:
        abort(400, 'Not a JSON')
    for k, v in params.items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(rev, k, v)
    return jsonify(rev.to_dict()), 200
