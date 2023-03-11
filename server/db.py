import configparser
import os
import pymongo
from flask import g
from gridfs import GridFS
config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(".ini")))

def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:
        client = pymongo.MongoClient(config['PROD']['DB_URI'])
        db = g._database = client.get_database('ecologyDB')

    return db


def get_grid_fs():
    db = get_db()

    fs = getattr(g, "_fs", None)

    if fs is None:
        fs = g._fs = GridFS(db)

    return fs