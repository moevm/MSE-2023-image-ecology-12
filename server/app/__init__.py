from flask import Flask
from .routes import api_bp
from flask_cors import CORS

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.register_blueprint(api_bp, url_prefix="/api")
CORS(app)
