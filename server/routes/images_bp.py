import os

import requests
from flask import Blueprint, jsonify, request, g, current_app, Response, send_file
from db import get_db, get_grid_fs
from werkzeug.local import LocalProxy
from bson.objectid import ObjectId
import io

db = LocalProxy(get_db)
fs = LocalProxy(get_grid_fs)
images_bp = Blueprint('images_bp', __name__, url_prefix="/images")


@images_bp.route('/', methods=['GET'])
def get_images_indexes():
    images = []
    for img in db.images.find({}):
        images.append({"id": str(img["_id"]), "name": img["name"]})

    return images


@images_bp.route('/tile_map_resource/<string:db_id>', methods=['GET'])
def index(db_id):
    return db.images.find_one(ObjectId(db_id))["tile_map_resource"]


worker_uri = os.environ['WORKER_URI'] if ('WORKER_URI' in os.environ) else "http://localhost:5001/"


@images_bp.route('/upload_image', methods=['POST'])
def add_image():
    """
        Adds a new image to the system for analysis.
    """
    image = request.files['image']
    file_id = fs.put(image, chunk_size=256 * 1024, filename=image.filename)
    item = {"filename": image.filename, "tile_map_resource": None, "fs_id": file_id, "name": request.form.get('name'), }
    db.images.insert_one(item)
    worker_res = requests.put(worker_uri + "slice/" + str(file_id))
    return jsonify({'message': 'Image added successfully'})


# Маршрут для leaflet-а, возвращает кусочки для отображения.
@images_bp.route("/tile/<string:db_id>/<int:z>/<int:x>/<int:y>", methods=['GET'])
def get_tile(db_id, z, x, y):
    image_name = db.images.find_one(ObjectId(db_id))["filename"]
    tile_info = fs.find_one({"filename": f"{image_name[:image_name.rfind('.')]}_{z}_{x}_{y}.png"})
    if (tile_info):
        tile = fs.get(tile_info._id).read()
        print(f"z - {z}, x - {x}, y - {y}")
        return send_file(io.BytesIO(tile), mimetype='image/png')


@images_bp.route('/<string:db_id>', methods=['GET'])
def get_image(db_id):
    image_info = db.images.find_one(ObjectId(db_id))
    image_file = fs.get(image_info["fs_id"])
    return send_file(io.BytesIO(image_file), mimetype='image/tiff')


@images_bp.route('/<string:db_id>/analysis', methods=['GET'])
def get_image_analysis(db_id):
    """
        Returns the results of the analysis for a specific image, including the detected deviations and their locations.
    """
    # analysis = ImageService.get_image_analysis(image_id)
    return jsonify({'analysis': []})  # jsonify(analysis)
