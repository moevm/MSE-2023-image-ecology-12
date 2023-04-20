from dataclasses import dataclass

import redis
import pymongo.database
from celery.signals import worker_process_init, worker_process_shutdown
from gridfs import GridFS

from app import config

@dataclass
class Local:
    db: pymongo.database.Database
    mapFs: GridFS
    tileFs: GridFS
    redis: redis.StrictRedis


local = Local(None, None, None, None)


@worker_process_init.connect
def init_worker(**kwargs):
    client = pymongo.MongoClient(config.MONGO_URI)
    local.db = client.get_database('ecologyDB')
    local.redisConn = redis.StrictRedis.from_url(config.REDIS_URI)
    local.mapFs = GridFS(local.db, 'map_fs')
    local.tileFs = GridFS(local.db, 'tile_fs')

    print('Initializing database connection for worker.')


@worker_process_shutdown.connect
def shutdown_worker(**kwargs):
    local.db.client.close()
    local.redis.close()

    print('Closing database connectionn for worker.')
