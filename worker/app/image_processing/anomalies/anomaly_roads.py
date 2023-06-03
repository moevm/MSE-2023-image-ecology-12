import cv2 as cv
import numpy as np
from bson import ObjectId

from app import app
from app.db import local
from app.image_processing.anomalies.anomaly_base import AnomalyBase
from app.image_processing.utility import connected_components, find_contours, get_image_RGB
import segmentation_models_pytorch as smp
import tensorflow as tf
# from onnx_tf.backend import prepare
# import onnxruntime
# import torch
# import albumentations as album


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
        # Useful to shortlist specific classes in datasets with large number of classes
        select_classes = ['background', 'road']
        select_class_indices = [['road', 'background'].index(cls.lower()) for cls in select_classes]
        select_class_rgb_values = np.array([[255, 255, 255], [0, 0, 0]])[select_class_indices]

        image_RGB = get_image_RGB(self.img_id, self.image_bytes)
        shape_image = image_RGB.shape
        img = cv.resize(image_RGB, (1024, 1024))
        image = cv.cvtColor(img, cv.COLOR_BGR2RGB)

        ENCODER = 'resnet50'
        ENCODER_WEIGHTS = 'imagenet'
        preprocessing_fn = smp.encoders.get_preprocessing_fn(ENCODER, ENCODER_WEIGHTS)
        image = preprocessing_fn(image)
        x_tensor = self._to_tensor(image)
        x_tensor = np.expand_dims(x_tensor, axis=0)

        self.update(10)
        input_name = local.roads_model.get_inputs()[0].name
        output_name = local.roads_model.get_outputs()[0].name
        outputs = local.roads_model.run([output_name], {input_name: x_tensor})
        pred_mask = outputs[0]

        self.update(20)
        pred_mask = tf.squeeze(pred_mask, axis=0).numpy()
        pred_mask = np.transpose(pred_mask, (1, 2, 0))
        pred_mask = self._colour_code_segmentation(self._reverse_one_hot(pred_mask), select_class_rgb_values)

        self.update(5)
        mask_8bit = cv.convertScaleAbs(pred_mask)
        gray_mask = cv.cvtColor(mask_8bit, cv.COLOR_BGR2GRAY)

        self.update(5)
        # Convert the mask to a binary mask using thresholding
        _, mask = cv.threshold(gray_mask, 127, 255, cv.THRESH_BINARY)

        mask = cv.resize(mask, (shape_image[1], shape_image[0]))

        contours = find_contours(mask)
        self.update(10)
        return contours

    # Perform reverse one-hot-encoding on labels / preds
    def _reverse_one_hot(self, image):
        """
        Transform a 2D array in one-hot format (depth is num_classes),
        to a 2D array with only 1 channel, where each pixel value is
        the classified class key.
        # Arguments
            image: The one-hot format image

        # Returns
            A 2D array with the same width and hieght as the input, but
            with a depth size of 1, where each pixel value is the classified
            class key.
        """
        x = np.argmax(image, axis=-1)
        return x

    def _to_tensor(self, x, **kwargs):
        return tf.cast(tf.transpose(x, perm=[2, 0, 1]), dtype=tf.float32)

    # Perform colour coding on the reverse-one-hot outputs
    def _colour_code_segmentation(self, image, label_values):
        """
        Given a 1-channel array of class keys, colour code the segmentation results.
        # Arguments
            image: single channel array where each value represents the class key.
            label_values

        # Returns
            Colour coded image for segmentation visualization
        """
        colour_codes = np.array(label_values)
        x = colour_codes[image.astype(int)]

        return x

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
