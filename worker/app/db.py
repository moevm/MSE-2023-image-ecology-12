from dataclasses import dataclass
import tensorflow as tf
from tensorflow.keras.models import load_model

import redis
import pymongo.database
from celery.signals import worker_process_init, worker_process_shutdown
from gridfs import GridFS

from app import config
import os

os.environ['SM_FRAMEWORK'] = "tf.keras"
import segmentation_models as sm


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
    local.redis = redis.StrictRedis.from_url(config.REDIS_URI, decode_responses=True)
    local.map_fs = GridFS(local.db, 'map_fs')
    local.tile_fs = GridFS(local.db, 'tile_fs')

    BACKBONE = 'resnet50'

    local.deforestation_model = load_model('app/image_processing/models/unet-attention-3d.hdf5')
    local.preprocessing_fn = sm.get_preprocessing(BACKBONE)
    local.roads_model = sm.Unet(BACKBONE, classes=1, activation='sigmoid')
    local.roads_model.load_weights('app/image_processing/models/unet_road.h5')
    print('Initializing database connection for worker.')


@worker_process_shutdown.connect
def shutdown_worker(**kwargs):
    local.db.client.close()
    local.redis.close()

    print('Closing database connection for worker.')
