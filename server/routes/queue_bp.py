from flask import Blueprint, jsonify, send_file, request
from db import get_db, get_grid_fs
from werkzeug.local import LocalProxy
from bson.objectid import ObjectId

queue_bp = Blueprint('queue', __name__, url_prefix='/queue')
db = LocalProxy(get_db)
fs = LocalProxy(get_grid_fs)
images_bp = Blueprint('images_bp', __name__)

#states: processing or paused or enqueued

@queue_bp.route('/add_to_queue/<string:db_id>', methods=['POST'])
def add_to_queue():
    """
        This route would be used to add images to the analysis queue for batch processing.
    """
    max_queue = db.images.find().sort({"queue": -1}).limit(1)
    db.images.update_one({'_id': db_id}, {"$set": { 'queue' : max_queue + 1}})
    return jsonify({'status': 'success'})

@queue_bp.route('/add_to_start_queue/<string:db_id>', methods=['POST'])
def add_to_start_queue():
    """
        This route would be used to add images to the analysis queue(in head) for batch processing.
    """

    count = 1
    for i in db.images.find({'status': 'enqueued'}):
        if db_id == i["_id"]:
            continue
        obj = ObjectId(i["_id"])
        db.images.update_one({"_id": obj}, {"$set": {'queue': count}})
        count += 1

    db.images.update_one({'_id': db_id}, {"$set": {'status': 'enqueued', 'queue': 0}})
    return jsonify({'status': 'success'})

@queue_bp.route('/update_queue', methods=['POST'])
def update_by_queue():
    """
        This route would be used to add images to the analysis queue for batch processing.
    """
    db_ids = request.get_json
    count = 0
    for i in db_ids:
        obj = ObjectId(i)
        db.images.update_one({"_id": obj}, {"$set": {'queue': count}})
        count += 1
    return jsonify({'status': 'success'})

@queue_bp.route('/<string:db_id>', methods=['GET'])
def get_queue():
    """
            This route would return the current state of the image analysis queue,
            including the number of images waiting to be processed and their estimated processing time.
    """
    # Return the current state of the analysis queue
    numbers = db.users.find({"state": "enqueued"}).count()
    all_time = numbers * 100 #TODO
    return jsonify({'queue': [numbers, all_time]})
