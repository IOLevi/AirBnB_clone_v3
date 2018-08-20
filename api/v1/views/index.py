from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status', strict_slashes=False)
def get_status():
    "returns status ok, 200"
    return jsonify({'status':'ok'}), 200
