import cv2
import numpy as np
from osgeo import gdal


def get_image_RGB(image_name, geotif_bytes):
    '''
    Преобразовывает tif файл в 3-х канальное 8-битное изображение и возвращает его, как массив numpy.

    geotif_bytes - путь до tif файла.
    '''
    gdal.FileFromMemBuffer("/vsimem/" + image_name, geotif_bytes)
    image = gdal.Open("/vsimem/" + image_name)

    # As, there are 3 bands, we will store in 3 different variables
    band_1 = image.GetRasterBand(1)  # red channel
    band_2 = image.GetRasterBand(2)  # green channel
    band_3 = image.GetRasterBand(3)  # blue channel

    b1 = band_1.ReadAsArray()
    b2 = band_2.ReadAsArray()
    b3 = band_3.ReadAsArray()

    # Normalize input image to range [0, 255]
    normalized_b1 = cv2.normalize(b1, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    normalized_b2 = cv2.normalize(b2, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    normalized_b3 = cv2.normalize(b3, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    del image
    gdal.Unlink("/vsimem/" + image_name)

    return np.dstack((normalized_b1, normalized_b2, normalized_b3))


def otsu_method(image_RGB, update):
    '''
    Метод Otsu выделения выделяющихся объектов на изображении. Возвращает контуры найденных объектов.

    image_RGB - 3-х канальное 8-битное изображение (преобразование изначального tif с помощью get_image_RGB).
    '''
    gray = cv2.cvtColor(image_RGB, cv2.COLOR_BGR2GRAY)
    update(12)

    # denoise the image with a Gaussian filter
    blurred_image = cv2.GaussianBlur(gray, (5, 5), 0)
    update(15)

    _, image_result = cv2.threshold(
        blurred_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )
    update(20)

    # Remove noise and fill holes in the binary image using morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20, 20))
    update(25)

    closed = cv2.morphologyEx(image_result, cv2.MORPH_OPEN, kernel)
    update(30)

    # Find the contours in the input image
    contours, _ = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)
    update(35)

    return contours
