from bson import ObjectId
from flask_cors import CORS
from flask import Flask
from bson.objectid import ObjectId
import threading
import queue
import sys
import os

from db import get_db, get_grid_fs
from image_processing.geotiff_slicer.slice2tiles import sliceToTiles

db = None
fs = None
app = Flask(__name__)
# Очередь на нарезку
q = queue.Queue()


# Обёртка для элементов очереди
class SlicerRequest:
    def __init__(self, function, arguments: dict):
        self.arguments = arguments
        self.function = function


# Обработчик
def slicer_work():
    while True:
        request_slicer = q.get()
        try:
            request_slicer.function(**request_slicer.arguments)
        except:
            # Чтобы не умирал поток в случае ошибки с одним запросом.
            print(f"Can't end function {request_slicer.function.__name__} with arguments {str(request_slicer.arguments)}", file=sys.stderr)


@app.route("/slice/<string:fs_id>", methods=["PUT"])
def slice_route(fs_id):
    q.put(SlicerRequest(slice, {"fs_id": fs_id}))
    return "Done"

def slice(fs_id):
    """
    Нарезать geotiff в базе данных с индексом id на кусочки и положить их в gridfs с именем 
    <image_name>_<z>_<x>_<y>.png
    """
    # Получаем запись из бд с информацией по изображению.s
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


if __name__ == "__main__":
    # Поток обработчика
    threading.Thread(target=slicer_work, daemon=True).start()

    CORS(app)
    port = os.environ['FLASK_PORT'] if ('FLASK_PORT' in os.environ) else 5002
    with app.app_context():
        db = get_db()
        fs = get_grid_fs()
    app.run(debug=True, host="0.0.0.0", port=port)
