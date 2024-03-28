from datetime import datetime

from flask import Blueprint, jsonify, request, send_file, abort
from redis.client import StrictRedis

from app.db import get_db, get_tile_fs, get_map_fs, get_redis

from werkzeug.local import LocalProxy
from bson.objectid import ObjectId
import io

from app.tasks import slice
from app.tasks import thresholding_otsu

from app import socketio

from app.tasks import (
    slice,
    thresholding_otsu,
    pipeline,
)


db = LocalProxy(get_db)
tile_fs = LocalProxy(get_tile_fs)
map_fs = LocalProxy(get_map_fs)
redis: StrictRedis = LocalProxy(get_redis)

scheduler_bp = Blueprint('scheluler', __name__, url_prefix="/scheduler")


@scheduler_bp.route('/schedule', methods=['POST'])
def schedule_task():
    pipeline.delay()

    return jsonify({'message': 'Image added successfully'})
