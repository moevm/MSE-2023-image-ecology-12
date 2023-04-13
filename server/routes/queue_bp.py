from flask import Blueprint, jsonify, send_file, request
from db import get_db, get_grid_fs
from werkzeug.local import LocalProxy
from bson.objectid import ObjectId
from bson.json_util import dumps
queue_bp = Blueprint('queue_bp', __name__, url_prefix='/queue')
db = LocalProxy(get_db)
fs = LocalProxy(get_grid_fs)

#states: processing or paused or enqueued


@queue_bp.route('/lower/<string:db_id>', methods=['PUT'])
def lower_queue(db_id):
    """
        Drops down in queue
    """
    db_id = ObjectId(db_id)
    queue_num = db.images.find_one({"_id": db_id})["queue"]
    max_value = db.images.find().sort({"queue": -1}).limit(1)["queue"]
    if db.images.find_one({"_id": db_id})["queue"] == max_value:
        return jsonify({'status': 'success'})

    next_id = None
    for i in db.images.find():
        if queue_num < i["queue"]:
            if next_id is None:
                next_id = i["_id"]
            else:
                if ObjectId(i["_id"])["queue"] > ObjectId(next_id["_id"])["queue"]:
                    next_id = i["_id"]

    buf = ObjectId(next_id["_id"])["queue"]
    db.images.update_one({"_id": next_id}, {"$set": {'queue': ObjectId(db_id["_id"])["queue"]}})
    db.images.update_one({"_id": db_id}, {"$set": {'queue': buf}})
    return jsonify({'status': 'success'})

@queue_bp.route('/higher/<string:db_id>', methods=['PUT'])
def higher_queue(db_id):
    """
        Drops up in queue
    """
    db_id = ObjectId(db_id)
    queue_num = db.images.find_one({"_id": db_id})["queue"]
    min_value = db.images.find().sort({"queue": 1}).limit(1)["queue"]
    if b.images.find_one({"_id": db_id})["queue"] == min_value:
        return jsonify({'status': 'success'})

    prev_id = None
    for i in db.images.find():
        if queue_num > i["queue"]:
            if prev_id is None:
                prev_id = i["_id"]
            else:
                if ObjectId(i["_id"])["queue"] < ObjectId(prev_id["_id"])["queue"]:
                    prev_id = i["_id"]

    buf = ObjectId(prev_id["_id"])["queue"]
    db.images.update_one({"_id": prev_id}, {"$set": {'queue': ObjectId(db_id["_id"])["queue"]}})
    db.images.update_one({"_id": db_id}, {"$set": {'queue': buf}})
    return jsonify({'status': 'success'})

@queue_bp.route('/down/<string:db_id>', methods=['PUT'])
def add_to_end_queue(db_id):
    """
        This route would be used to add images to the analysis queue for batch processing.
    """
    db_id = ObjectId(db_id)
    max_value = db.images.find().sort({"queue": -1}).limit(1)["queue"]
    if b.images.find_one({"_id": db_id})["queue"] == max_value:
        return jsonify({'status': 'success'})
    db.images.update_one({'_id': db_id}, {"$set": {'queue': max_value + 1}})
    return jsonify({'status': 'success'})

@queue_bp.route('/up/<string:db_id>', methods=['PUT'])
def add_to_start_queue(db_id):
    """
        This route would be used to add images to the analysis queue(in head) for batch processing.
    """
    db_id = ObjectId(db_id)
    min_value = db.images.find().sort({"queue": 1}).limit(1)["queue"]
    if b.images.find_one({"_id": db_id})["queue"] == min_value:
        return jsonify({'status': 'success'})

    for i in db.images.find({'status': 'enqueued'}):
        if db_id == i["_id"]:
            continue
        obj = ObjectId(i["_id"])
        db.images.update_one({"_id": obj}, {"$set": {'queue': i["queue"] + 1}})

    db.images.update_one({'_id': db_id}, {"$set": {'queue': min_value}})
    return jsonify({'status': 'success'})

@queue_bp.route('/get_queue', methods=['GET'])
def get_queue():
    """
            This route would return the current state of the image analysis queue,
            including the number of images waiting to be processed and their estimated processing time.
    """
    d = []
    for i in db.images.find():
        d.append({"id": str(i["_id"]),
                  "uploadDate": i["date_upload"],
                  "progress": i["progress"],
                  "status": i["state"],
                  "name": i["name"]})
    return dumps(d)
