from tensorflow.keras.models import load_model
from app.image_processing.find_forest.helpers import morph_operations, find_contours
import numpy as np
import cv2

model = load_model('app/image_processing/models/unet-attention-3d.hdf5')


def find_deforestation(image_RGP, update):
    shape_image = image_RGP.shape
    resized_image = cv2.resize(image_RGP, (512, 512))
    update(12)
    image_norm = resized_image / 255
    update(15)
    prediction = model.predict(image_norm.reshape(1, 512, 512, 3))
    update(20)
    mask = (np.round(prediction[0])).astype(np.uint8)
    update(22)
    denoised_img = morph_operations(mask, update)
    denoised_img = cv2.resize(denoised_img, (shape_image[1], shape_image[0]))
    update(30)
    contour_img = find_contours(denoised_img)
    update(35)

    return contour_img
