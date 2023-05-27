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
        img_anomalies_types = img["anomalies"]
        for img_anomalies in img_anomalies_types:
            if (img_anomalies['name'] != 'Forest'):
                for i in range(len(img_anomalies['area'])):
                    anomalies.append({
                        "id": str(img["_id"]),
                        "name": img_anomalies["name"],
                        "anomalyIndex": i,
                        "area": img_anomalies['area'][i],
                        "uploadDate": img["upload_date"],
                        "detectDate": img["detect_date"]
                    })
    return anomalies


@anomalies_bp.route('/<string:img_id>/<string:anomaly_name>/<string:anomaly_index>', methods=['GET'])
def get_anomaly(img_id, anomaly_name, anomaly_index):
    img = db.images.find_one(ObjectId(img_id))
    img_anomalies_types = img["anomalies"]
    area = 0
    for img_anomalies in img_anomalies_types:
        if (img_anomalies['name'] == anomaly_name):
            area = img_anomalies['area'][int(anomaly_index)]
    result = {
        "reportId": "0", #TODO
        "id": str(img_id),
        "name": anomaly_name,
        "anomalyIndex": anomaly_index,
        "area": area,
        "uploadDate": img["upload_date"],
        "detectDate": img["detect_date"] 
    }
    return result
