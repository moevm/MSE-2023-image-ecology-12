from bson import ObjectId
from app import app
from app.image_processing.coordinates_transform.transform_coordinates import CoordintesTransformer
from app.image_processing.find_forest.otsu_method import get_image_RGB, find_forest
from app.db import local
import tensorflow as tf
from tensorflow.keras.models import load_model
import cv2
import numpy as np


@app.task(name='thresholding_otsu', queue="image_process")
def thresholding_otsu(img_id: str):
    print("fdsfs____________________________________________________________")
    """
    Метод Оцу включает в себя преобразование изображения в двоичный формат,
    где пиксели классифицируются как («полезные» и «фоновые»),
    рассчитывая такой порог, чтобы внутриклассовая дисперсия была минимальной.
    """
    db = local.db
    map_fs = local.map_fs
    redis = local.redis

    # Получаем запись из бд с информацией по изображению.
    image_info = db.images.find_one(ObjectId(img_id))
    queue_item = f'queue:{img_id}'

    redis.hset(queue_item, 'status', 'processing')

    update = lambda x: redis.hset(queue_item, 'progress', x)

    # Получаем саму картинку из GridFS.
    image_bytes = map_fs.get(ObjectId(image_info['fs_id'])).read()
    update(3)

    image_RGB = get_image_RGB(img_id, image_bytes)

    redis.hset(queue_item, 'progress', 30)
    
    coord_transformer = CoordintesTransformer(image_bytes)
    redis.hset(queue_item, 'progress', 40)
    print("40============")
    contures = find_forest(image_RGB, update)
    print("50=================")
    polygon_lat_long = []
    for line in contures:

        # Преобразовываем координаты каждой точки из пикселей в широту и долготу.
        line_arr = []
        for point in line:
            x_pix, y_pix = point[0]
            line_arr.append(coord_transformer.pixel_xy_to_lat_long(x_pix, y_pix))
        polygon_lat_long.append(line_arr)
        update(progress := progress + d)

    coord_transformer.close()
    update(100)

    # Добавим полученные контуры в базу данных.
    db.images.update_one({"_id": image_info["_id"]}, {"$set": {"forest_polygon": polygon_lat_long}})

    redis.delete(queue_item)
    db.images.update_one({"_id": image_info["_id"]}, {"$set": {"ready": True}})

    return "Done"
