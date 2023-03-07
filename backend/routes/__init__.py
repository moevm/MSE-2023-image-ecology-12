from flask import Blueprint
from .images_bp import images_bp
from .search_bp import search_bp
from .queue_bp import queue_bp


api_bp = Blueprint('api', __name__)
api_bp.register_blueprint(images_bp, url_prefix="/images")
api_bp.register_blueprint(search_bp, url_prefix="/search")
api_bp.register_blueprint(queue_bp, url_prefix="/queue")
