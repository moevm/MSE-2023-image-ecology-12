import time

from bson import ObjectId
from app import app
from app.image_processing.compress_image.compress import compress
from app.image_processing.crop_image.crop import crop_image
from app.db import local


@app.task(name='pipeline', queue='pipeline')
def pipeline(img_id: str):
    db = local.db
    map_fs = local.map_fs
    redis = local.redis

    image_info = db.images.find_one(ObjectId(img_id))
    queue_item = f'queue:{img_id}'

    redis.hset(queue_item, 'status', 'processing')
    update = lambda x: redis.hset(queue_item, 'progress', x)

    # Получаем саму картинку из GridFS.
    image_bytes = map_fs.get(ObjectId(image_info['fs_id'])).read()
    time.sleep(10)
    update(10)
    # redis.hset(queue_item, 'status', 'compressing')
    compresses_bytes = compress(image_bytes)
    time.sleep(10)
    update(20)
    # redis.hset(queue_item, 'status', 'cropping')
    cropped_byte = crop_image(compresses_bytes, 0, 0, 100, 100)
    update(30)
    time.sleep(10)
    redis.delete(f'slice_queue:{img_id}')
    # raise Exception(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>test<<<<<<<<<<<<<<<< {len(cropped_byte)}')
    return "Done"
