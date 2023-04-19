# from werkzeug.local import LocalProxy
#
# from app import app
# from server.app.db import get_db, get_tile_fs, get_map_fs
# import slice
# import image_process
#
# db = LocalProxy(get_db)
# tileFs = LocalProxy(get_tile_fs())
# mapFs = LocalProxy(get_map_fs())
#
#
# @app.task
# def delete_all_data_in_db_and_fs():
#     db.images.drop()
#     tileFs.files.drop()
#     tileFs.chunks.drop()
#     mapFs.files.drop()
#     mapFs.chunks.drop()
#
#     print('All database data deleted.')
#
#
# @app.task
# def add_test_data_db():
#     imagesCollection = db.images
#
#     files = ["map_samples/1.tif", "map_samples/2.tif"]
#     for imageName in files:
#         if (not mapFs.exists({"filename": imageName})):
#             with open(imageName, 'rb') as f:
#                 contents = f.read()
#             fs_image_id = mapFs.put(contents, filename=imageName)
#
#             # tile_map_resource - XML информация дополнительная, для правильных координат отображения тайлов.
#             item = {
#                 "filename": imageName,
#                 "tile_map_resource": None,
#                 "fs_id": fs_image_id,
#                 "forest_polygon": None,
#                 "name": imageName[:imageName.rfind(".")]
#             }
#
#             imagesCollection.insert_one(item)
#
#         # Если картинка есть в бд, а её tile_map_resource нет (это означает, что нарезка еще не производилась).
#         if (not db.images.find_one({"filename": imageName}) == None and
#                 db.images.find_one({"filename": imageName})["tile_map_resource"] == None):
#             fs_image_id = db.images.find_one({"filename": imageName})["fs_id"]
#
#             # Отдаем запрос worker-у (тестовый) на нарезку сохраненного в бд файла.
#             worker_res = slice.slice.delay(fs_image_id)  # requests.put(worker_url + "slice/" + str(fs_image_id))
#
#         # Если картинка есть в бд, а её forest_polygon нет (это означает, что обработка еще не производилась).
#         if (not db.images.find_one({"filename": imageName}) == None and
#                 db.images.find_one({"filename": imageName})["forest_polygon"] == None):
#             fs_image_id = db.images.find_one({"filename": imageName})["fs_id"]
#
#             # Отдаем запрос worker-у (тестовый) на нахождение леса на снимке.
#             worker_res = image_process.thresholding_otsu.delat(
#                 fs_image_id)  # requests.put(worker_url + "thresholding_otsu/" + str(fs_image_id))
