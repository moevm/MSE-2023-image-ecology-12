from flask import Blueprint, jsonify
from db import get_db
from werkzeug.local import LocalProxy
from bson import json_util
from datetime import datetime, timedelta
import json


db = LocalProxy(get_db)
search_bp = Blueprint('search', __name__, url_prefix='/search')


@search_bp.route('/test')
def index():
    return """
        <form method="POST" action="/api/search/search_images" enctype="multipart/form-data">
            <input type='text' name="date">
            <input type="submit">
        </form> 
    """

@search_bp.route('/search_images/<string:date>', methods=['GET'])
def search_images(date):
    """
        Allows users to search for specific images by date, location, and other metadata.
    """
    date = datetime.fromisoformat(date)
    documents = db['images'].find({'uploadDate': {'$gte': date, '$lt': date + timedelta(days=1)}})
    documents = [{'_id': str(document['_id']),
                  'filename': document.get('filename', None),
                  'tile_map_resource': document.get('tile_map_resource', None),
                  'fs_id': str(document['fs_id']),
                  'uploadDate': document.get('uploadDate', None)} for document in documents]
    # Search for specific images
    print(documents)
    return jsonify(documents)
