from flask import Blueprint, jsonify, request, send_file
from app.db import get_db, get_tile_fs, get_map_fs

from werkzeug.local import LocalProxy
from bson.objectid import ObjectId
import io

from app.tasks import slice
from app.tasks import thresholding_otsu

db = LocalProxy(get_db)
tile_fs = LocalProxy(get_tile_fs)
map_fs = LocalProxy(get_map_fs)

images_bp = Blueprint('images_bp', __name__, url_prefix="/images")


@images_bp.route('/', methods=['GET'])
def get_images_indexes():
    images = []
    for img in db.images.find({}):
        images.append({
            "id": str(img["_id"]),
            "name": img["name"],
        })

    return images


@images_bp.route('/tile_map_resource/<string:db_id>', methods=['GET'])
def index(db_id):
    return db.images.find_one(ObjectId(db_id))["tile_map_resource"]


@images_bp.route('/upload_image', methods=['POST'])
def add_image():
    image = request.files['image']
    file_id = map_fs.put(image, filename=image.filename, chunk_size=256 * 1024)
    item = {
        "filename": image.filename,
        "tile_map_resource": None,
        "fs_id": file_id,
        "forest_polygon": None,
        "name": request.form.get('name')
    }

    db.images.insert_one(item)
    slice.delay(str(file_id))
    thresholding_otsu.delay(str(file_id))
    return jsonify({'message': 'Image added successfully'})


# Маршрут для leaflet-а, возвращает кусочки для отображения.
@images_bp.route("/tile/<string:db_id>/<int:z>/<int:x>/<int:y>", methods=['GET'])
def get_tile(db_id, z, x, y):
    image_name = db.images.find_one(ObjectId(db_id))["filename"]
    tile_info = tile_fs.find_one({"filename": f"{image_name[:image_name.rfind('.')]}_{z}_{x}_{y}.png"})
    if (tile_info):
        tile = tile_fs.get(tile_info._id).read()
        return send_file(io.BytesIO(tile), mimetype='image/png')
    else:
        return 'OK'


@images_bp.route('/<string:db_id>', methods=['GET'])
def get_image(db_id):
    image_info = db.images.find_one(ObjectId(db_id))
    image_file = tile_fs.get(image_info["fs_id"])
    return send_file(io.BytesIO(image_file), mimetype='image/tiff')


@images_bp.route('/forest/<string:db_id>', methods=['GET'])
def get_image_forest(db_id):
    image_info = db.images.find_one(ObjectId(db_id))
    return image_info["forest_polygon"]


@images_bp.route('/<string:db_id>/analysis', methods=['GET'])
def get_image_analysis(db_id):
    # analysis = ImageService.get_image_analysis(image_id)
    return jsonify({'analysis': []})  # jsonify(analysis)
