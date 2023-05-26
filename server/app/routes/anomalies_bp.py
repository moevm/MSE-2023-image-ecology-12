import io
from flask import Blueprint, send_file
from redis.client import StrictRedis
from werkzeug.local import LocalProxy
from bson.objectid import ObjectId


from app.db import get_db, get_tile_fs, get_map_fs, get_redis

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

