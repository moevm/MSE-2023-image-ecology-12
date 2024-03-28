from flask import Blueprint, jsonify

queue_bp = Blueprint('queue', __name__, url_prefix='/queue')


@queue_bp.route('/', methods=['POST'])
def add_to_queue():
    """
    This route would be used to add images to the analysis queue for batch processing.
    """
    # Add an image to the analysis queue
    return jsonify({'status': 'success'})


@queue_bp.route('/', methods=['GET'])
def get_queue():
    """
    This route would return the current state of the image analysis queue,
    including the number of images waiting to be processed and their estimated processing time.
    """
    # Return the current state of the analysis queue
    return jsonify({'queue': []})
