from bson import ObjectId

from .celery_app import app
from app.image_processing.coordinates_transform.transform_coordinates import CoordintesTransformer
from app.image_processing.find_forest.otsu_method import get_image_RGB, otsu_method

from .db import local


@app.task
def thresholding_otsu(fs_id):
    """
    Метод Оцу включает в себя преобразование изображения в двоичный формат,
    где пиксели классифицируются как («полезные» и «фоновые»),
    рассчитывая такой порог, чтобы внутриклассовая дисперсия была минимальной.
    """
    db = local.db
    mapFs = local.mapFs
    tileFs = local.tileFs

    # Получаем запись из бд с информацией по изображению.
    image_info = db.images.find_one({"fs_id": ObjectId(fs_id)})
    # Получаем саму картинку из GridFS.
    image_bytes = mapFs.get(ObjectId(fs_id)).read()
    # Нарезаем на фрагменты.
    image_name = image_info["filename"]

    image_RGB = get_image_RGB(image_name, image_bytes)

    coord_transformer = CoordintesTransformer(image_bytes)

    polygon_lat_long = []
    for line in otsu_method(image_RGB):
        # Преобразовываем координаты каждой точки из пикселей в широту и долготу.
        line_arr = []
        for point in line:
            x_pix, y_pix = point[0]
            line_arr.append(coord_transformer.pixel_xy_to_lat_long(x_pix, y_pix))
        polygon_lat_long.append(line_arr)

    coord_transformer.close()

    # Добавим полученные контуры в базу данных.
    db.images.update_one({"_id": image_info["_id"]}, {"$set": {"forest_polygon": polygon_lat_long}})

    return "Done"
