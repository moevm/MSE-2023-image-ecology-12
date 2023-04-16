import os
import pymongo
from flask import g
from gridfs import GridFS


def init_db():
    print("Init db")
    return get_db()


def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:
        DB_URI = os.environ['DB_URI'] if ('DB_URI' in os.environ) else "mongodb://localhost:27017/db"
        client = pymongo.MongoClient(DB_URI)  # config['PROD']['DB_URI']
        # Если есть база данных ecologyDB
        db = g._database = client.get_database('ecologyDB')

    return db


def close_db(error=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def get_grid_fs():
    db = get_db()

    fs = getattr(g, "_fs", None)

    if fs is None:
        fs = g._fs = GridFS(db)

    return fs


def get_worker_url():
    if 'worker_url' not in g:
        g.worker_uri = os.environ['WORKER_URI'] if ('WORKER_URI' in os.environ) else "http://localhost:5001/"
    return g.worker_uri


def get_slicer_url():
    if 'slicer_url' not in g:
        g.slicer_url = os.environ['SLICER_URI'] if ('SLICER_URI' in os.environ) else "http://localhost:5002/"
    return g.slicer_url
