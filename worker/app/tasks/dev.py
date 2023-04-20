from app import app
from app.tasks.slice import slice
from app.tasks.image_process import thresholding_otsu
from app.db import local


@app.task(name='delete_all_data_in_db_and_fs')
def delete_all_data_in_db_and_fs():
    local.db.client.drop_database('ecologyDB')
    print('All database data deleted.')


@app.task(name='add_test_data_db')
def add_test_data_db():
    db = local.db
    mapFs = local.mapFs
    tileFs = local.tileFs

    imagesCollection = db.images

    files = ["map_samples/1.tif", "map_samples/2.tif"]
    for imageName in files:
        if (not mapFs.exists({"filename": imageName})):
            with open(imageName, 'rb') as f:
                contents = f.read()
            fs_image_id = mapFs.put(contents, filename=imageName)

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
            slice.delay(str(fs_image_id))

        # Если картинка есть в бд, а её forest_polygon нет (это означает, что обработка еще не производилась).
        if (not db.images.find_one({"filename": imageName}) == None and
                db.images.find_one({"filename": imageName})["forest_polygon"] == None):
            fs_image_id = db.images.find_one({"filename": imageName})["fs_id"]

            # Отдаем запрос worker-у (тестовый) на нахождение леса на снимке.
            thresholding_otsu.delay(str(fs_image_id))
