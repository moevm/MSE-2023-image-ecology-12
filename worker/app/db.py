import redis
import pymongo
from celery.signals import worker_process_init, worker_process_shutdown
from gridfs import GridFS
from werkzeug.local import Local

from app import config

local = Local()


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
    local.redisConn.close()

    print('Closing database connectionn for worker.')
