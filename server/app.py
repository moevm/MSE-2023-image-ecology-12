from flask import Flask
from routes import api_bp
from flask_cors import CORS
import os
from db import init_db


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_bp, url_prefix="/api")
    CORS(app)
    with app.app_context():
        init_db()
    return app


if __name__ == "__main__":
    application = create_app()
    application.config['DEBUG'] = True
    port = os.environ['FLASK_PORT'] if ('FLASK_PORT' in os.environ) else 5000
    application.run(host='0.0.0.0', port=port)
