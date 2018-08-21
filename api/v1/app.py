from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")

@app.teardown_appcontext
def tear_down(self):
    "tears down"
    storage.close()

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    app.run(host=os.getenv("HBNB_API_HOST") if os.getenv("HBNB_API_HOST") else "0.0.0.0", port=os.getenv("HBNB_API_PORT") if os.getenv("HBNB_API_PORT") else 5000, threaded=True)
