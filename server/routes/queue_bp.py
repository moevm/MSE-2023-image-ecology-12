from flask import Blueprint, jsonify, request, g, current_app, Response, send_file
from db import get_db, get_grid_fs
from werkzeug.local import LocalProxy
from bson.objectid import ObjectId
import io

queue_bp = Blueprint('queue', __name__, url_prefix='/queue')


@queue_bp.route('/<image_id>', methods=['POST'])
def add_to_queue():
    """
        This route would be used to add images to the analysis queue for batch processing.
    """
    # Add an image to the analysis queue
    return jsonify({'status': 'success'})

@images_bp.route('/<image_id>', methods=['GET'])
def get_image(image_id):
    image_file = fs.get(ObjectId(image_id))
    return send_file(image_file, mimetype='image/tiff')

@queue_bp.route('/', methods=['GET'])
def get_queue():
    """
            This route would return the current state of the image analysis queue,
            including the number of images waiting to be processed and their estimated processing time.
    """
    # Return the current state of the analysis queue
    return jsonify({'queue': []})
