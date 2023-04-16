import os
import pymongo
from flask import g
from gridfs import GridFS


def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:
        # client = pymongo.MongoClient(config['PROD']['DB_URI'])
        DB_URI = os.environ['DB_URI'] if ('DB_URI' in os.environ) else "mongodb://localhost:27017/db"
        client = pymongo.MongoClient(DB_URI)
        # Если есть базад
        db = g._database = client.get_database('ecologyDB')


    return db


def get_grid_fs():
    db = get_db()

    fs = getattr(g, "_fs", None)

    if fs is None:
        fs = g._fs = GridFS(db)

    return fs
