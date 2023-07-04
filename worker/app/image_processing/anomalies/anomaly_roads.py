<<<<<<< HEAD
import cv2
=======
import cv2 as cv
>>>>>>> add6ff44010833186681f7d90f11119a32594fd0
import numpy as np
from bson import ObjectId

from app import app
from app.db import local
from app.image_processing.anomalies.anomaly_base import AnomalyBase
from app.image_processing.utility import connected_components, find_contours, get_image_RGB


class AnomalyRoads(AnomalyBase):
    '''
        Класс для нахождения дорог на изображении.
    '''

    def __init__(self, img_id, image_bytes):
        super().__init__(img_id, image_bytes)

        self.name = 'Roads'
        self.color = 'red'

    def find_contours_of_anomaly(self):
        '''
        Использование нейросети для нахождения областей дорог.
        '''

        image_RGB = get_image_RGB(self.img_id, self.image_bytes)
        shape_image = image_RGB.shape
        img = cv2.resize(image_RGB, (512, 512))
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image = local.preprocessing_fn(image)
        image = np.expand_dims(image, axis=0)
        self.update(10)
        pr_mask = local.roads_model.predict(image).round()
        pr_mask = pr_mask[..., 0].squeeze()
        pr_mask = (pr_mask * 255).astype(np.uint8)
        self.update(20)
        # Find the contours in the input image
        # contours, _ = cv2.findContours(pr_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        contours = find_contours(pr_mask)
        areas = [cv2.contourArea(contour) for contour in contours]
        mean_area = np.mean(areas)
        pr_mask = connected_components(pr_mask,
                                       threshold_area=mean_area,
                                       threshold_width=10,
                                       threshold_height=10)
        self.update(10)
        pr_mask = cv2.resize(pr_mask, (shape_image[1], shape_image[0]))
        contours = find_contours(pr_mask)
        self.update(10)
        return contours


    @staticmethod
    @app.task(name='roads_find', queue="image_process")
    def create_and_process(img_id):
        db = local.db
        map_fs = local.map_fs
        image_info = db.images.find_one(ObjectId(img_id))

        # Получаем саму картинку из GridFS.
        image_bytes = map_fs.get(ObjectId(image_info['fs_id'])).read()

        roads_anomaly = AnomalyRoads(img_id, image_bytes)
        AnomalyBase.process_anomaly(roads_anomaly)
        roads_anomaly.filter_polygons_by_area(10)
        roads_anomaly.after_end_of_process()
        return "Processing completed"
