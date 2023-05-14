from bson import ObjectId
from app import app
from app.image_processing.coordinates_transform.transform_coordinates import CoordintesTransformer
from app.image_processing.find_forest.otsu_method import otsu_method
from app.image_processing.find_forest.deforestation import find_deforestation
from app.image_processing.find_forest.helpers import get_image_RGB
from app.db import local
# from werkzeug.local import LocalProxy
#
# db = local.db
# # tile_fs = LocalProxy(get_tile_fs)
# map_fs = local.map_fs
# redis = local.redis


@app.task(name='thresholding_otsu', queue="image_process")
def thresholding_otsu(img_id: str):
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

    update = lambda x: redis.hset(queue_item, 'progress', float(redis.hget(f'queue:{img_id}', 'progress')) + x)

    # Получаем саму картинку из GridFS.
    image_bytes = map_fs.get(ObjectId(image_info['fs_id'])).read()
    update(1)

    image_RGB = get_image_RGB(img_id, image_bytes)
    update(2)

    coord_transformer = CoordintesTransformer(image_bytes)
    update(3)

    lines = otsu_method(image_RGB, update)

    d = 40 / len(lines)
    polygon_lat_long = []
    for line in lines:
        # Преобразовываем координаты каждой точки из пикселей в широту и долготу.
        line_arr = []
        for point in line:
            x_pix, y_pix = point[0]
            line_arr.append(coord_transformer.pixel_xy_to_lat_long(x_pix, y_pix))
        polygon_lat_long.append(line_arr)
        update(d)

    coord_transformer.close()

    # Добавим полученные контуры в базу данных.
    db.images.update_one({"_id": image_info["_id"]}, {"$set": {"forest_polygon": polygon_lat_long}})

    redis.hset(queue_item, 'processing_functions', int(redis.hget(queue_item, 'processing_functions')) - 1)
    if int(redis.hget(queue_item, 'processing_functions')) == 0:
        redis.delete(queue_item)
        db.images.update_one({"_id": image_info["_id"]}, {"$set": {"ready": True}})

    return "Done"


@app.task(name='deforestation', queue="image_process")
def deforestation(img_id: str):
    """
    Нахождение вырубков с помощью нейронной сети Attention Unet
    """
    db = local.db
    map_fs = local.map_fs
    redis = local.redis

    # Получаем запись из бд с информацией по изображению.
    image_info = db.images.find_one(ObjectId(img_id))
    queue_item = f'queue:{img_id}'

    redis.hset(queue_item, 'status', 'processing')

    update = lambda x: redis.hset(queue_item, 'progress', float(redis.hget(f'queue:{img_id}', 'progress')) + x)

    # Получаем саму картинку из GridFS.
    image_bytes = map_fs.get(ObjectId(image_info['fs_id'])).read()
    update(1)

    image_RGB = get_image_RGB(img_id, image_bytes)
    update(2)

    coord_transformer = CoordintesTransformer(image_bytes)
    update(3)

    lines = find_deforestation(image_RGB, update)

    d = 40 / len(lines)
    polygon_lat_long = []
    for line in lines:
        # Преобразовываем координаты каждой точки из пикселей в широту и долготу.
        line_arr = []
        for point in line:
            x_pix, y_pix = point[0]
            line_arr.append(coord_transformer.pixel_xy_to_lat_long(x_pix, y_pix))
        polygon_lat_long.append(line_arr)
        update(d)

    coord_transformer.close()

    # Добавим полученные контуры в базу данных.
    db.images.update_one({"_id": image_info["_id"]}, {"$set": {"deforestation_polygon": polygon_lat_long}})

    redis.hset(queue_item, 'processing_functions', int(redis.hget(queue_item, 'processing_functions')) - 1)
    if int(redis.hget(queue_item, 'processing_functions')) == 0:
        redis.delete(queue_item)
        db.images.update_one({"_id": image_info["_id"]}, {"$set": {"ready": True}})

    return "Done"