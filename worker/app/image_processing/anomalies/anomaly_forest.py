import cv2
import numpy as np
from bson import ObjectId
from PIL import Image

from app import app
from app.db import local
from app.image_processing.anomalies.anomaly_base import AnomalyBase
from app.image_processing.utility import morph_operations, find_contours, get_image_RGB,\
    find_forest, connected_components_for_points, otsu_method
from celery.utils.log import get_task_logger
import os
logger = get_task_logger(__name__)


class AnomalyForest(AnomalyBase):
    '''
    Класс для нахождения леса на изображении.
    '''
    def __init__(self, img_id, image_bytes):
        super().__init__(img_id, image_bytes)
        
        self.name = 'Forest'
        self.color = 'green'
    
    def find_contours_of_anomaly(self):
        '''
        Нахождение леса на изображении. Возвращает контуры найденных объектов.
        '''
        print("FIND FOREST STARTED")
        print("find forest is running")
        image_RGB = get_image_RGB(self.img_id, self.image_bytes)
        h, w = image_RGB.shape[0], image_RGB.shape[1]
        print("image_RGB получено")
        image_np = image_RGB[:, :, :3].copy()
        print("image_np получено")
        binary_image = find_forest(image_RGB)
        point_coords = connected_components_for_points(binary_image)
        if len(point_coords) == 0:
            print("LANGSAM STARTED")
            text_prompt = 'forest'

            image_pill = Image.fromarray(image_np)
            print("image_pill получено")
            self.update(20)
            src_image = 'app/image_processing/images/output.tif'
            image_pill.save(src_image)
            print('image_pill saved; predict started')
            if os.path.exists(src_image):
                print('Файл output.tif найден')
            else:
                print('Файл не найден')
            self.update(10)
            local.lang_sam.predict(
                src_image,
                text_prompt=text_prompt,
                box_threshold=0.24,
                text_threshold=0.24)
            print('predict finished')
            prediction = local.lang_sam.prediction.copy()
            prediction = (prediction - prediction.min()) / (prediction.max() - prediction.min()) * 255
            prediction = prediction.astype('uint8')
            self.update(10)
        else:
            print("SAM started")
            local.sam.set_image(image_np)
            print("Image saved; predict started")
            masks, scores, logits = local.sam.predict(point_coords=point_coords,
                                                      return_results=True)
            print("Predict finished")
            index = np.argmax(scores, axis=0)
            logit = logits[index]
            logit = (logit - logit.min()) / (logit.max() - logit.min()) * 255
            logit = logit.astype('uint8')
            print("logit выполнено")
            prediction = otsu_method(logit, is_gray=True)
            print("otsu finished")
        # Find the contours in the input image
        prediction = cv2.resize(prediction, (w, h))
        print('contours search finished')
        contours = find_contours(prediction)  # prediction
        self.update(10)
        return contours
    
    @staticmethod
    @app.task(name='forest_find', queue="image_process")
    def create_and_process(img_id):
        db = local.db
        map_fs = local.map_fs
        image_info = db.images.find_one(ObjectId(img_id))

        # Получаем саму картинку из GridFS.
        image_bytes = map_fs.get(ObjectId(image_info['fs_id'])).read()

        forest_anomaly = AnomalyForest(img_id, image_bytes)
        AnomalyBase.process_anomaly(forest_anomaly)
        forest_anomaly.filter_polygons_by_area(10)
        forest_anomaly.after_end_of_process()
        return "Processing completed"
