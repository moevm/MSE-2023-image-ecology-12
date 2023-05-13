from dataclasses import dataclass
import redis
import pymongo.database
from celery.signals import worker_process_init, worker_process_shutdown
from gridfs import GridFS
from app import config


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
    
    
    from app.image_processing.find_forest.EfficientNetModel import EfficientNetModel 
    local.model_forest = EfficientNetModel(input_shape=(64, 64, 3), num_classes=1)
    local.model_forest.load_model('app/image_processing/models/efficientB2_model.h5')
    print('Initializing database connection for worker.')


@worker_process_shutdown.connect
def shutdown_worker(**kwargs):
    local.db.client.close()
    local.redis.close()
    print('Closing database connection for worker.')
