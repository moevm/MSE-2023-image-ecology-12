from dataclasses import dataclass
from tensorflow.keras.models import load_model
import onnx
from onnx_tf.backend import prepare
import onnxruntime

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
    local.redis = redis.StrictRedis.from_url(config.REDIS_URI, decode_responses=True)
    local.map_fs = GridFS(local.db, 'map_fs')
    local.tile_fs = GridFS(local.db, 'tile_fs')

    local.deforestation_model = load_model('app/image_processing/models/unet-attention-3d.hdf5')
    # init roads
    # roads_model = onnx.load("model_roads.onnx")
    # roads_model = prepare(roads_model)
    session_roads = onnxruntime.InferenceSession("app/image_processing/models/model_roads.onnx")
    local.roads_model = session_roads
    print('Initializing database connection for worker.')


@worker_process_shutdown.connect
def shutdown_worker(**kwargs):
    local.db.client.close()
    local.redis.close()

    print('Closing database connection for worker.')
