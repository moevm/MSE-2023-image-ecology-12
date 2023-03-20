from flask import Flask
from routes import api_bp
from flask_cors import CORS
import requests
import os

from db import init_db, get_db, get_grid_fs

from pprint import pprint


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_bp, url_prefix="/api")
    CORS(app)
    with app.app_context():
        init_db()
    return app

def add_test_data_db(app: Flask, worker_uri):
    with app.app_context():
        db = get_db()
        fs = get_grid_fs()
    imageName = "sample.tif"
    imagesCollection = db.images

    if (not fs.exists({"filename": imageName})):
        with open(imageName, 'rb') as f:
            contents = f.read()
        fs_image_id = fs.put(contents, filename=imageName)

        # tile_map_resource - XML информация дополнительная, для правильных координат отображения тайлов.
        item = {"filename": imageName, "tile_map_resource": None, "fs_id": fs_image_id}
        imagesCollection.insert_one(item)

        # Отдаем запрос worker-у (тестовый) на нарезку сохраненного в бд файла.
        worker_res = requests.put(worker_uri + "slice/" + str(fs_image_id))

    # # Тест
    print("-"*100)
    print("<-> Images collection:")
    cursor = imagesCollection.find({})
    for document in cursor: 
        pprint(document)

    # print("-"*100)
    # print("<-> GridFS files collection:")
    # cursor = fs.find({})
    # for document in cursor: 
    #     pprint(document.filename)


if __name__ == "__main__":
    worker_uri = os.environ['WORKER_URI'] if ('WORKER_URI' in os.environ) else "http://localhost:5001/"
    application = create_app()
    add_test_data_db(application, worker_uri)
    application.config['DEBUG'] = True
    port = os.environ['FLASK_PORT'] if ('FLASK_PORT' in os.environ) else 5000
    application.run(host='0.0.0.0', port=port)
