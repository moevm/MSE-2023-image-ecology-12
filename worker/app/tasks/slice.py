import os
from bson.objectid import ObjectId
from app import app
from app.image_processing.geotiff_slicer.slice2tiles import sliceToTiles
from celery.utils.log import get_task_logger
from app.db import local

logger = get_task_logger(__name__)


@app.task(name='slice')
def slice(fs_id):
    """
    Нарезать geotiff в базе данных с индексом id на кусочки и положить их в gridfs с именем
    <image_name>_<z>_<x>_<y>.png
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
    sliceToTiles(image_name, image_bytes, "./" + image_name[:image_name.rfind(".")])

    # Удаляем фрагменты, если они уже были в GridFS.
    cursor = db.fs.files.find({"filename": {"$regex": image_name[:image_name.rfind(".")] + "_\d*_\d*_\d*.png"}})
    for document in cursor:
        tileFs.delete(document["_id"])

    # Добавляем все фрагменты в GridFS.
    for root, _, files in os.walk(image_name[:image_name.rfind(".")]):
        path = root.split(os.sep)
        for file in files:
            # Сами фрагменты лежат по пути /{z}/{x}/{y}.png, но нужно отсечь доп. файлы
            # с информацией о геолокации в корне папки.
            if (len(path) >= 2):
                with open(root + "/" + file, "rb") as f:
                    file_content = f.read()

                tileFs.put(file_content, filename="_".join(path) + "_" + file)

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
