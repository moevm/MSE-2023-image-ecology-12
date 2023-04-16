from flask import Flask
from routes import api_bp
from flask_cors import CORS
import requests
import os

from db import init_db, get_grid_fs, get_worker_url


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_bp, url_prefix="/api")
    CORS(app)
    with app.app_context():
        db = init_db()
        fs = get_grid_fs()
        worker_url = get_worker_url()
    return app, db, fs, worker_url


def delete_all_data_in_db_and_fs(app: Flask, db):
    db.images.drop()
    db.fs.files.drop()
    db.fs.chunks.drop()

    print('All database data deleted.')


def add_test_data_db(app: Flask, db, fs, worker_url):
    imagesCollection = db.images

    files = ["1.tif", "2.tif"]
    for imageName in files:
        if (not fs.exists({"filename": imageName})):
            with open(imageName, 'rb') as f:
                contents = f.read()
            fs_image_id = fs.put(contents, filename=imageName)

            # tile_map_resource - XML информация дополнительная, для правильных координат отображения тайлов.
            item = {
                "filename": imageName, 
                "tile_map_resource": None, 
                "fs_id": fs_image_id, 
                "forest_polygon": None, 
                "name": imageName[:imageName.rfind(".")]
            }

            imagesCollection.insert_one(item)

        # Если картинка есть в бд, а её tile_map_resource нет (это означает, что нарезка еще не производилась).
        if (not db.images.find_one({"filename": imageName}) == None and
                db.images.find_one({"filename": imageName})["tile_map_resource"] == None):
            fs_image_id = db.images.find_one({"filename": imageName})["fs_id"]

            # Отдаем запрос worker-у (тестовый) на нарезку сохраненного в бд файла.
            worker_res = requests.put(worker_url + "slice/" + str(fs_image_id))

        # Если картинка есть в бд, а её forest_polygon нет (это означает, что обработка еще не производилась).
        if (not db.images.find_one({"filename": imageName}) == None and
                db.images.find_one({"filename": imageName})["forest_polygon"] == None):
            fs_image_id = db.images.find_one({"filename": imageName})["fs_id"]

            # Отдаем запрос worker-у (тестовый) на нахождение леса на снимке.
            worker_res = requests.put(worker_url + "thresholding_otsu/" + str(fs_image_id))

def print_old_db():
    print("-"*100)
    print("<-> Images collection:")
    with application.app_context():
        db = get_db()
    cursor = db.images.find({})
    for document in cursor: 
        pprint(document)
    print("-"*100)


if __name__ == "__main__":
    worker_uri = os.environ['WORKER_URI'] if ('WORKER_URI' in os.environ) else "http://localhost:5001/"
    application, db, fs, worker_url = create_app()
    # Очистка базы данных                       
    # delete_all_data_in_db_and_fs(application, db)  
    # Тестовые данные                                     
    # add_test_data_db(application, db, fs, worker_url)
    # Вывод существующих записей в бд в при запуске
    # print_old_db()
    application.config['DEBUG'] = True
    port = os.environ['FLASK_PORT'] if ('FLASK_PORT' in os.environ) else 5000
    application.run(host='0.0.0.0', port=port)
