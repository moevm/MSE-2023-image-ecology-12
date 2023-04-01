import cv2
from bson import ObjectId
from flask_cors import CORS
# from sdd_segmentation.sdd import sdd_threshold_selection
from flask import Flask, jsonify, request, send_file
from werkzeug.local import LocalProxy
from bson.objectid import ObjectId
import numpy as np
import os

from db import get_db, get_grid_fs
from image_processing.geotiff_slicer.slice2tiles import sliceToTiles

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
            # Сами фрагменты лежат по пути /{z}/{x}.png, но нужно отсечь доп. файлы
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



@app.route("/thresholding_otsu", methods=["GET"])  # POST !!!
def thresholding_otsu():
    """
    Метод Оцу включает в себя преобразование изображения в двоичный формат,
    где пиксели классифицируются как («полезные» и «фоновые»), 
    рассчитывая такой порог, чтобы внутриклассовая дисперсия была минимальной.
    """
    # data = request.get_json()
    image_id = "640c7feb44e959620e519270"  # data['image_id']
    image_file = fs.get(ObjectId(image_id))

    # Load the GeoTiff image
    # input_image = cv2.imread(image_file, cv2.IMREAD_UNCHANGED)
    # Read the image data from the file
    image_data = image_file.read()

    # Decode the image data to a NumPy array
    input_image = cv2.imdecode(np.frombuffer(image_data, np.uint16), cv2.IMREAD_UNCHANGED)

    # Normalize input image to range [0, 255]
    normalized_image = cv2.normalize(input_image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    # Convert normalized image to 8-bit image
    image = cv2.convertScaleAbs(normalized_image)

    # Applying Otsu's method setting the flag value into cv.THRESH_OTSU.
    # Use a bimodal image as an input.
    # Optimal threshold value is determined automatically.
    otsu_threshold, image_result = cv2.threshold(
        image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU,
    )

    # Remove noise and fill holes in the binary image using morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20, 20))
    closed = cv2.morphologyEx(image_result, cv2.MORPH_OPEN, kernel)

    # Find the contours in the input image
    contours, hierarchy = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # Draw the contours on an image
    contour_img = cv2.drawContours(image, contours, -1, (255, 255, 255), 2)

    # AttributeError: 'numpy.ndarray' object has no attribute 'read'
    # Преобразовать nummpy arrray в байтовой последовательность
    # file_id = fs.put(contour_img, filename=image_file.filename + "_otsu", chunk_size=256 * 1024)
    # print(file_id)
    # return send_file(image_file, mimetype='image/tif')
    # Display the image
    cv2.imshow("Contours", contour_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Run the app on local host and port 8989
    CORS(app)
    port = os.environ['FLASK_PORT'] if ('FLASK_PORT' in os.environ) else 5001
    app.run(debug=True, host="0.0.0.0", port=port)
