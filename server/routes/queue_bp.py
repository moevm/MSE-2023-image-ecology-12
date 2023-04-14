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
    obj_queue = db.images.find_one({"_id": db_id})["queue"]
    max_value = db.images.find().sort("queue", -1).limit(1)[0]["queue"]
    if db.images.find_one({"_id": db_id})["queue"] == max_value:
        return jsonify({'status': 'success'})

    next_obj = None
    for i in db.images.find():
        if obj_queue < i["queue"]:
            if next_obj is None:
                next_obj = i
            else:
                if i["queue"] > next_obj["queue"]:
                    next_obj = i

    buf = next_obj["queue"]
    db.images.update_one({"_id": next_obj["_id"]}, {"$set": {'queue': db.images.find_one({"_id": db_id})["queue"]}})
    db.images.update_one({"_id": db_id}, {"$set": {'queue': buf}})
    return jsonify({'status': 'success'})

@queue_bp.route('/higher/<string:db_id>', methods=['PUT'])
def higher_queue(db_id):
    """
        Drops up in queue
    """
    db_id = ObjectId(db_id)
    obj_queue = db.images.find_one({"_id": db_id})["queue"]
    min_value = db.images.find().sort("queue", 1).limit(1)[0]["queue"]
    if db.images.find_one({"_id": db_id})["queue"] == min_value:
        return jsonify({'status': 'success'})

    prev_obj = None
    for i in db.images.find():
        if obj_queue > i["queue"]:
            if prev_obj is None:
                prev_obj = i
            else:
                if i["queue"] < prev_obj["queue"]:
                    prev_obj = i

    buf = prev_obj["queue"]
    db.images.update_one({"_id": prev_obj["_id"]}, {"$set": {'queue':  db.images.find_one({"_id": db_id})["queue"]}})
    db.images.update_one({"_id": db_id}, {"$set": {'queue': buf}})
    return jsonify({'status': 'success'})

@queue_bp.route('/down/<string:db_id>', methods=['PUT'])
def add_to_end_queue(db_id):
    """
        This route would be used to add images to the analysis queue for batch processing.
    """
    db_id = ObjectId(db_id)
    max_value = db.images.find().sort("queue", -1).limit(1)[0]["queue"]
    if db.images.find_one({"_id": db_id})["queue"] == max_value:
        return jsonify({'status': 'success'})
    db.images.update_one({'_id': db_id}, {"$set": {'queue': max_value + 1}})
    return jsonify({'status': 'success'})

@queue_bp.route('/up/<string:db_id>', methods=['PUT'])
def add_to_start_queue(db_id):
    """
        This route would be used to add images to the analysis queue(in head) for batch processing.
    """
    db_id = ObjectId(db_id)
    min_value = db.images.find().sort("queue", 1).limit(1)[0]["queue"]
    if db.images.find_one({"_id": db_id})["queue"] == min_value:
        return jsonify({'status': 'success'})

    for i in db.images.find():
        if db_id == i["_id"]:
            continue
        obj = i
        db.images.update_one({"_id": obj["_id"]}, {"$set": {'queue': i["queue"] + 1}})

    db.images.update_one({'_id': db_id}, {"$set": {'queue': min_value}})
    return jsonify({'status': 'success'})

@queue_bp.route('/get_queue', methods=['GET'])
def get_queue():
    """
            This route would return the current state of the image analysis queue,
            including the number of images waiting to be processed and their estimated processing time.
    """
    d = []
    for i in db.images.find().sort("queue", 1):
        d.append({"id": str(i["_id"]),
                  "uploadDate": i["date_upload"],
                  "progress": i["progress"],
                  "status": i["state"],
                  "name": i["name"]})
    return dumps(d)
