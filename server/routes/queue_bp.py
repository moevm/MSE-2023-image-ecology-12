from flask import Blueprint, jsonify, request, g, current_app, Response, send_file
from db import get_db, get_grid_fs
from werkzeug.local import LocalProxy
from bson.objectid import ObjectId
import io
from pymongo import updateOne

queue_bp = Blueprint('queue', __name__, url_prefix='/queue')
db = LocalProxy(get_db)
fs = LocalProxy(get_grid_fs)
images_bp = Blueprint('images_bp', __name__)

@queue_bp.route('/<string:db_id>', methods=['POST'])
def add_to_queue():
    """
        This route would be used to add images to the analysis queue for batch processing.
    """
    max_queue = db.images.find().sort({"queue": -1}).limit(1)
    db.images.updateOne({'_id': db_id}, {"$set": { 'queue' : max_queue + 1}})
    return jsonify({'status': 'success'})

@queue_bp.route('/<string:db_id>', methods=['POST'])
def add_to_begin_queue():
    """
        This route would be used to add images to the analysis queue(in head) for batch processing.
    """

    db.images.updateOne({'_id': db_id}, {"$set": {'status': 'paused'}})
    db.images.updateMany({'status': 'processing'}, {"$set": {'queue': 'paused'}})

    count = 1
    for i in db.images.find({'status': 'processing'}):
        obj_image = ObjectId(i["_id"])
        db.images.update_one({"_id": obj_image}, {"$set": {'queue': count}})
        count += 1

    db.images.updateOne({'_id': db_id}, {"$set": {'status': 'processing', 'queue': 0}})
    return jsonify({'status': 'success'})

@queue_bp.route('/<list<string>:db_ids>', methods=['POST'])
def down_in_queue():
    """
        This route would be used to add images to the analysis queue for batch processing.
    """
    max_queue = db.images.find().sort({"queue": -1}).limit(1)
    db.images.updateOne({'_id': db_id}, {"$set": { 'queue' : max_queue + 1}})
    return jsonify({'status': 'success'})

@queue_bp.route('/<list<string>:db_ids>', methods=['POST'])
def up_in_queue():
    """
        This route would be used to add images to the analysis queue for batch processing.
    """
    max_queue = db.images.find().sort({"queue": -1}).limit(1)
    db.images.updateOne({'_id': db_id}, {"$set": { 'queue' : max_queue + 1}})
    return jsonify({'status': 'success'})

@images_bp.route('/<string:db_id>', methods=['GET'])
def get_image(image_id):
    image_file = fs.get(ObjectId(image_id))
    return send_file(image_file, mimetype='image/tiff')

@queue_bp.route('/<string:db_id>', methods=['GET'])
def get_queue():
    """
            This route would return the current state of the image analysis queue,
            including the number of images waiting to be processed and their estimated processing time.
    """
    # Return the current state of the analysis queue
    numbers = len(db.users.find({"state": "enqueued"})) #processing, paused, enqueued
    all_time = numbers * 100 #TODO
    return jsonify({'queue': [numbers, all_time]})
