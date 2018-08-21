from flask import jsonify, request, Response, abort
from api.v1.views import app_views
from models import storage
import json
from models.place import Places

@app_views.route('cities/<city_id>/places', strict_slashes=False, methods=['GET'])
def get_all_cities(city_id):
    ''' gets all places in a city '''
