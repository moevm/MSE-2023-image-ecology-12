from flask import Blueprint, jsonify, request, g, current_app, Response, send_file
from db import get_db, get_grid_fs
from werkzeug.local import LocalProxy
from bson.objectid import ObjectId


db = LocalProxy(get_db)
fs = LocalProxy(get_grid_fs)
images_bp = Blueprint('images_bp', __name__)


@images_bp.route('/test')
def index():
    return """
        <form method="POST" action="/api/images/upload_image" enctype="multipart/form-data">
            <input type="file" name="image">
            <input type="submit">
        </form> 
    """


@images_bp.route('/upload_image', methods=['POST'])
def add_image():
    """
        Adds a new image to the system for analysis.
    """
    image = request.files['image']
    file_id = fs.put(image, filename=image.filename, chunk_size=256*1024)
    return jsonify({'message': 'Image added successfully'})


@images_bp.route('/<image_id>', methods=['GET'])
def get_image(image_id):
    image_file = fs.get(ObjectId(image_id))
    return send_file(image_file, mimetype='image/tiff')


@images_bp.route('/<image_id>/analysis', methods=['GET'])
def get_image_analysis(image_id):
    """
        Returns the results of the analysis for a specific image, including the detected deviations and their locations.
    """
    # analysis = ImageService.get_image_analysis(image_id)
    return jsonify({'analysis': []})  # jsonify(analysis)
