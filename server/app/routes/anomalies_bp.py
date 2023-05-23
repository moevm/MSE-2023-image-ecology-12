from datetime import datetime

from flask import Blueprint, jsonify, request, send_file, abort
from redis.client import StrictRedis

from app.db import get_db, get_tile_fs, get_map_fs, get_redis

from werkzeug.local import LocalProxy
from bson.objectid import ObjectId
import io

from app.tasks import slice
from app.tasks import thresholding_otsu
from app.tasks import deforestation

from app import socketio

db = LocalProxy(get_db)
tile_fs = LocalProxy(get_tile_fs)
map_fs = LocalProxy(get_map_fs)
redis: StrictRedis = LocalProxy(get_redis)

anomalies_bp = Blueprint('anomalies_bp', __name__, url_prefix="/anomalies")


@anomalies_bp.route('/', methods=['GET'])
def get_anomalies_list():
    anomalies = []
    for img in db.images.find({}):
        #Надо продумать хранение аномалий, потому что это хардкод в чистом виде :(
        anomalies.append({
            "id": str(img["_id"]),
            "area": 123, #TODO img["anomaly_name"]["area"]
            "upload_date": img["upload_date"],
            "detected_date": img["upload_date"],
        })
    if len(anomalies) == 0:
        anomalies = [{
            "id": "1",
            "area": 123, #TODO img["anomaly_name"]["area"]
            "upload_date": "2023-03-03T13:03:03",
            "detected_date": "2023-03-03T13:03:03"
        }]
    return anomalies

@anomalies_bp.route('/<string:img_id>', methods=['GET'])
def get_anomaly(img_id):
    image_info = db.images.find_one(ObjectId(img_id))
    image_file = tile_fs.get(image_info["fs_id"])
    return send_file(io.BytesIO(image_file), mimetype='image/tiff')

