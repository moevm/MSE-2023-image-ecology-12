from dataclasses import dataclass
from samgeo import text_sam
from samgeo import SamGeo
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
from tensorflow.keras.models import load_model
import redis
import pymongo.database
from celery.signals import worker_process_init, worker_process_shutdown, worker_init, celeryd_init
from gridfs import GridFS
from celery.utils.log import get_task_logger
from app.image_processing.find_forest.EfficientNetModel import EfficientNetModel
from app import config

os.environ['SM_FRAMEWORK'] = "tf.keras"
import segmentation_models as sm


logger = get_task_logger(__name__)


@dataclass
class Local:
    db: pymongo.database.Database
    map_fs: GridFS
    tile_fs: GridFS
    redis: redis.StrictRedis
    # is_model_loaded: bool


local = Local(None, None, None, None)


@celeryd_init.connect
def capture_worker_name(sender, **kwargs):
    logger.info("capture_worker_name")
    os.environ["WORKER_NAME"] = '{0}'.format(sender)
    logger.info("WORKER NAME: {}".format(os.environ["WORKER_NAME"]))


@worker_init.connect
def load_models(**kwargs):
    logger.info("WORKER INIT")
    logger.info("WORKER NAME: {}".format(os.environ["WORKER_NAME"]))
    if os.environ["WORKER_NAME"] == 'celery@worker_image_process':
        logger.info('loading deforestation model')
        local.deforestation_model = load_model('app/image_processing/models/unet-attention-3d.hdf5')
        BACKBONE = 'resnet50'
        local.preprocessing_fn = sm.get_preprocessing(BACKBONE)
        local.roads_model = sm.Unet(BACKBONE, classes=1, activation='sigmoid')
        local.roads_model.load_weights('app/image_processing/models/unet_road.h5')
        logger.info('loading EfficientNetModel')
        local.model_forest = EfficientNetModel(input_shape=(64, 64, 3), num_classes=1)
        local.model_forest.load_model('app/image_processing/models/efficientB2_model.h5')
        logger.info('loading SamGeo')
        local.sam = SamGeo(
                model_type="vit_h",
                checkpoint="app/image_processing/models/sam_vit_h_4b8939.pth",
                automatic=False,
                sam_kwargs=None,
        )
        logger.info('loading LangSAM')
        local.lang_sam = text_sam.LangSAM()


@worker_process_init.connect
def init_worker(**kwargs):
    client = pymongo.MongoClient(config.MONGO_URI)
    local.db = client.get_database('ecologyDB')
    local.redis = redis.StrictRedis.from_url(config.REDIS_URI, decode_responses=True)
    local.map_fs = GridFS(local.db, 'map_fs')
    local.tile_fs = GridFS(local.db, 'tile_fs')
    print('Initializing database connection for worker.')


@worker_process_shutdown.connect
def shutdown_worker(**kwargs):
    local.db.client.close()
    local.redis.close()

    print('Closing database connection for worker.')
