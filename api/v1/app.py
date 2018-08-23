#!/usr/bin/python3
"App module"
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views, url_prefix="/api/v1")
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def tear_down(self):
    "tears down"
    storage.close()


@app.errorhandler(404)
def not_found(error):
    "error handler for 404"
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(
            host=os.getenv("HBNB_API_HOST") if os.getenv("HBNB_API_HOST")
            else "0.0.0.0",
            port=int(
                os.getenv("HBNB_API_PORT")) if os.getenv("HBNB_API_PORT")
            else 5000, threaded=True)
