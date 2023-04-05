from flask import Flask
from routes import api_bp
from flask_cors import CORS
import requests
import os

from db import init_db, get_db, get_grid_fs


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_bp, url_prefix="/api")
    CORS(app)
    with app.app_context():
        init_db()
    return app

def delete_all_data_in_db_and_fs(app: Flask):
    with app.app_context():
        db = get_db()

    db.images.drop()
    db.fs.files.drop()
    db.fs.chunks.drop()

def add_test_data_db(app: Flask, worker_uri):
    with app.app_context():
        db = get_db()
        fs = get_grid_fs()
    imagesCollection = db.images

    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for imageName in files:
        if (imageName[(imageName.rfind(".") + 1):] in ["tif", "tiff"] and not fs.exists({"filename": imageName})):
            with open(imageName, 'rb') as f:
                contents = f.read()
            fs_image_id = fs.put(contents, filename=imageName)

            # tile_map_resource - XML информация дополнительная, для правильных координат отображения тайлов.
            item = {"filename": imageName, "tile_map_resource": None, "fs_id": fs_image_id, "forest_polygon": None}
            imagesCollection.insert_one(item)

        # Если картинка есть в бд, а её tile_map_resource нет (это означает, что нарезка еще не производилась).
        if (not db.images.find_one({"filename": imageName}) == None and 
            db.images.find_one({"filename": imageName})["tile_map_resource"] == None):
            fs_image_id = db.images.find_one({"filename": imageName})["fs_id"]

            # Отдаем запрос worker-у (тестовый) на нарезку сохраненного в бд файла.
            worker_res = requests.put(worker_uri + "slice/" + str(fs_image_id))

        # Если картинка есть в бд, а её forest_polygon нет (это означает, что обработка еще не производилась).
        if (not db.images.find_one({"filename": imageName}) == None and 
            db.images.find_one({"filename": imageName})["forest_polygon"] == None):
            fs_image_id = db.images.find_one({"filename": imageName})["fs_id"]

            # Отдаем запрос worker-у (тестовый) на нахождение леса на снимке.
            worker_res = requests.put(worker_uri + "thresholding_otsu/" + str(fs_image_id))


if __name__ == "__main__":
    worker_uri = os.environ['WORKER_URI'] if ('WORKER_URI' in os.environ) else "http://localhost:5001/"
    application = create_app()
    # Раскоментируй эту строчку, если хочешь очистить базу данных при запуске сервера (тестовый режим).                                 
    delete_all_data_in_db_and_fs(application)
    add_test_data_db(application, worker_uri)
    application.config['DEBUG'] = True
    port = os.environ['FLASK_PORT'] if ('FLASK_PORT' in os.environ) else 5000
    application.run(host='0.0.0.0', port=port)
