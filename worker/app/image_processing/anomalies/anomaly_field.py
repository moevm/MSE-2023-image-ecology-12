import cv2
from bson import ObjectId

from app import app
from app.db import local
from app.image_processing.anomalies.anomaly_base import AnomalyBase
from app.image_processing.utility import morph_operations, find_contours, get_image_RGB


class AnomalyField(AnomalyBase):
    """
    Класс для нахождения полей на изображении.
    """

    def __init__(self, img_id, image_bytes):
        super().__init__(img_id, image_bytes)

        self.name = 'Field'
        self.color = 'green'

    def find_contours_of_anomaly(self):
        """
        Возвращает контуры найденных объектов.
        """
        image_RGB = get_image_RGB(self.img_id, self.image_bytes)
        gray = cv2.cvtColor(image_RGB, cv2.COLOR_BGR2GRAY)
        image_median = cv2.medianBlur(gray, 5)

        self.update(10)

        t_lower = 50  # Lower Threshold
        t_upper = 100  # Upper threshold
        L2Gradient = True

        # Applying the Canny Edge filter with L2Gradient = True
        image_canny = cv2.Canny(image_median, t_lower, t_upper, L2gradient=L2Gradient)

        self.update(20)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
        image_morph = cv2.dilate(image_canny, kernel)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
        image_morph = cv2.morphologyEx(image_morph, cv2.MORPH_CLOSE, kernel)
        image_morph_inv = cv2.bitwise_not(image_morph)
        image_morph_inv = cv2.copyMakeBorder(image_morph_inv, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0)

        contours = find_contours(image_morph_inv)
        self.update(10)

        areas = [cv2.contourArea(contour) for contour in contours]
        mean_area = np.mean(areas)
        threshold_area = mean_area

        # remove regions that are too small
        filtered_contours = [contour for contour in contours if cv2.contourArea(contour) > threshold_area]

        self.update(10)
        return filtered_contours

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
