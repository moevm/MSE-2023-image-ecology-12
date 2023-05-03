import cv2
from helpers import morph_operations, find_contours


def otsu_method(image_RGB, update):
    '''
    Метод Otsu выделения выделяющихся объектов на изображении. Возвращает контуры найденных объектов.
    
    image_RGB - 3-х канальное 8-битное изображение (преобразование изначального tif с помощью get_image_RGB).
    '''
    gray = cv2.cvtColor(image_RGB, cv2.COLOR_BGR2GRAY)
    update(12)

    # denoise the image with a Gaussian filter
    blurred_image = cv2.GaussianBlur(gray,(5,5),0)
    update(15)

    otsu_threshold, image_result = cv2.threshold(
        blurred_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU,
    )
    update(20)

    # Remove noise and fill holes in the binary image using morphological operations
    closed = morph_operations(image_result, update, use_gaussian_filter=False)
    update(30)

    # Find the contours in the input image
    contours = find_contours(closed)
    update(35)
    return contours
