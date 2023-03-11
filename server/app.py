from flask import Flask
from routes import api_bp
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_bp, url_prefix="/api")
    CORS(app)
    return app


if __name__ == "__main__":
    application = create_app()
    application.config['DEBUG'] = True
    # application.config['MONGO_URI'] = config['PROD']['DB_URI']

    application.run()
