from bson import ObjectId
from flask_cors import CORS
from flask import Flask
from werkzeug.local import LocalProxy
from bson.objectid import ObjectId
import os

from db import get_db, get_grid_fs
from image_processing.geotiff_slicer.slice2tiles import sliceToTiles
from image_processing.find_forest.otsu_method import get_image_RGB, otsu_method
from image_processing.coordinates_transform.transform_coordinates import CoordintesTransformer

db = LocalProxy(get_db)
fs = LocalProxy(get_grid_fs)
# Init the app
app = Flask(__name__)


@app.route("/slice/<string:fs_id>", methods=["PUT"])
def slice(fs_id):
    """
    Нарезать geotiff в базе данных с индексом id на кусочки и положить их в gridfs с именем 
    <image_name>_<z>_<x>_<y>.png
    """
    # Получаем запись из бд с информацией по изображению.
    image_info = db.images.find_one({"fs_id": ObjectId(fs_id)})
    # Получаем саму картинку из GridFS.
    image_bytes = fs.get(ObjectId(fs_id)).read()
    # Нарезаем на фрагменты.
    image_name = image_info["filename"]
    sliceToTiles(image_name, image_bytes, "./" + image_name[:image_name.rfind(".")])

    # Удаляем фрагменты, если они уже были в GridFS.
    cursor = db.fs.files.find({"filename": {"$regex": image_name[:image_name.rfind(".")] + "_\d*_\d*_\d*.png"}})
    for document in cursor:
        fs.delete(document["_id"])

    # Добавляем все фрагменты в GridFS.
    for root, _, files in os.walk(image_name[:image_name.rfind(".")]):
        path = root.split(os.sep)
        for file in files:
            # Сами фрагменты лежат по пути /{z}/{x}/{y}.png, но нужно отсечь доп. файлы
            # с информацией о геолокации в корне папки.
            if (len(path) >= 2):
                with open(root + "/" + file, "rb") as f:
                    file_content = f.read()
                
                fs.put(file_content, filename="_".join(path) + "_" + file)

    # Добавляем данные для отображения изображения.
    with open(image_name[:image_name.rfind(".")] + "/" + "tilemapresource.xml", "r") as f:
        xml_content = f.read()
    db.images.update_one({"_id": image_info["_id"]}, {"$set": {"tile_map_resource": xml_content}})
    
    # Удаляем временную папку с слайсами.
    for root, dirs, files in os.walk(image_name[:image_name.rfind(".")], topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(image_name[:image_name.rfind(".")])

    return "Done"


@app.route("/thresholding_otsu/<string:fs_id>", methods=["PUT"])
def thresholding_otsu(fs_id):
    """
    Метод Оцу включает в себя преобразование изображения в двоичный формат,
    где пиксели классифицируются как («полезные» и «фоновые»), 
    рассчитывая такой порог, чтобы внутриклассовая дисперсия была минимальной.
    """
    # Получаем запись из бд с информацией по изображению.
    image_info = db.images.find_one({"fs_id": ObjectId(fs_id)})
    # Получаем саму картинку из GridFS.
    image_bytes = fs.get(ObjectId(fs_id)).read()
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


if __name__ == "__main__":
    # Run the app on local host and port 8989
    CORS(app)
    port = os.environ['FLASK_PORT'] if ('FLASK_PORT' in os.environ) else 5001
    app.run(debug=True, host="0.0.0.0", port=port)
