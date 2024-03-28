from dataclasses import dataclass

import pymongo.database
import redis
from app import config
from celery.signals import worker_process_init, worker_process_shutdown
from gridfs import GridFS


@dataclass
class Local:
    db: pymongo.database.Database
    map_fs: GridFS
    tile_fs: GridFS
    redis: redis.StrictRedis


local = Local(None, None, None, None)


@worker_process_init.connect
def init_worker(**kwargs):
    client = pymongo.MongoClient(config.MONGO_URI)
    local.db = client.get_database('ecologyDB')
    local.redis = redis.StrictRedis.from_url(config.REDIS_URI)
    local.map_fs = GridFS(local.db, 'map_fs')
    local.tile_fs = GridFS(local.db, 'tile_fs')

    print('Initializing database connection for worker.')


@worker_process_shutdown.connect
def shutdown_worker(**kwargs):
    local.db.client.close()
    local.redis.close()

    print('Closing database connection for worker.')
