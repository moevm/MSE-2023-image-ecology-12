from datetime import datetime

from flask import Blueprint, jsonify, request, send_file, abort
from redis.client import StrictRedis

from app.db import get_db, get_tile_fs, get_map_fs, get_redis

from werkzeug.local import LocalProxy
from bson.objectid import ObjectId
import io

from app.tasks import (
    slice,
    thresholding_otsu,
    pipeline,
)

from app import socketio

db = LocalProxy(get_db)
tile_fs = LocalProxy(get_tile_fs)
map_fs = LocalProxy(get_map_fs)
redis: StrictRedis = LocalProxy(get_redis)

images_bp = Blueprint('images_bp', __name__, url_prefix="/images")


@images_bp.route('/', methods=['GET'])
def get_images_list():
    images = []
    for img in db.images.find({}):
        images.append({
            "id": str(img["_id"]),
            "name": img["name"],
            'size': map_fs.find_one({'_id': img["fs_id"]}).length,
            "ready": img["ready"],
            "sliced": img["sliced"]
        })

    return images


@images_bp.route('/tile_map_resource/<string:img_id>', methods=['GET'])
def index(img_id):
    tile_map_resource = db.images.find_one(ObjectId(img_id))["tile_map_resource"]
    if tile_map_resource is None:
        abort(404)
    else:
        return db.images.find_one(ObjectId(img_id))["tile_map_resource"]


@images_bp.route('/upload_image', methods=['POST'])
def add_image():
    image = request.files['image']
    file_id = map_fs.put(image, filename=image.filename, chunk_size=256 * 1024)
    img_name = request.form.get('name')
    item = {
        "tile_map_resource": None,
        "fs_id": file_id,
        "forest_polygon": None,
        "name": img_name,
        'ready': False,
        'sliced': False
    }

    result = db.images.insert_one(item)
    img_id = result.inserted_id

    redis.hset(f'queue:{img_id}', mapping={
        'id': str(img_id),
        'progress': 0,
        'name': img_name,
        'uploadDate': datetime.now().isoformat(),
        'status': 'enqueued'
    })

    redis.hset(f'slice_queue:{img_id}', mapping={'id': str(img_id)})

    slice.delay(str(img_id))
    thresholding_otsu.delay(str(img_id))

    return jsonify({'message': 'Image added successfully'})


@images_bp.route('/delete_image/<string:img_id>', methods=['DELETE'])
def delete_image(img_id):
    image_info = db.images.find_one(ObjectId(img_id))
    if (image_info):
        fs_id = image_info["fs_id"]

        db.images.delete_one({"_id": ObjectId(img_id)})

        map_fs.delete(fs_id)
        for tile in tile_fs.find({"image_id": ObjectId(img_id)}):
            tile_fs.delete(tile._id)

        socketio.emit("images", get_images_list())
        return jsonify({'message': 'Image deleted successfully'})
    return 'OK'


# Маршрут для leaflet-а, возвращает кусочки для отображения.
@images_bp.route("/tile/<string:img_id>/<int:z>/<int:x>/<int:y>", methods=['GET'])
def get_tile(img_id, z, x, y):
    tile = tile_fs.find_one({'image_id': ObjectId(img_id), 'z': z, 'x': x, 'y': y})
    if tile:
        return send_file(io.BytesIO(tile.read()), mimetype='image/png')
    else:
        return 'OK'


@images_bp.route('/<string:img_id>', methods=['GET'])
def get_image(img_id):
    image_info = db.images.find_one(ObjectId(img_id))
    image_file = tile_fs.get(image_info["fs_id"])
    return send_file(io.BytesIO(image_file), mimetype='image/tiff')


@images_bp.route('/forest/<string:img_id>', methods=['GET'])
def get_image_forest(img_id):
    image_info = db.images.find_one(ObjectId(img_id))["forest_polygon"]
    if (image_info is None):
        abort(404)
    else:
        return image_info


@images_bp.route('/<string:img_id>/analysis', methods=['GET'])
def get_image_analysis(img_id):
    # analysis = ImageService.get_image_analysis(image_id)
    return jsonify({'analysis': []})  # jsonify(analysis)
