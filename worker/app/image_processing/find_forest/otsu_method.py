import cv2
import numpy as np
from osgeo import gdal
import tensorflow as tf
from app.image_processing.coordinates_transform.transform_coordinates import CoordintesTransformer
from app.db import local

    
input_size = (64, 64)


def check_block_within_bounds(shape, block_size, lrx, lry, ulx, uly):
    print("check")
    x_shape, y_shape = shape[0], shape[1]

    if lrx > x_shape:
        lrx = x_shape
        ulx = lrx - block_size
    if lry > y_shape:
        lry = y_shape
        uly = lry - block_size
    print("after check")
    return lrx, lry, ulx, uly

def predict_block(block, threshold):
    print("block")
    image = cv2.resize(block, input_size)
    print("block 1")
    image = image.astype('float32') / 255.0 
    print("block 2")
    prediction = local.model.predict(np.expand_dims(image, axis = 0))
    print("block 3")
    predicted_label = 1 if prediction.item() >= threshold else 0
    print("after block")
    return predicted_label


def find_forest(img, update):
    block_size = 64
    table_size = 8
    threshold = 0.25
    print("________in otsu 1________")
    binary_image = otsu_method(img, update)
    print("_____after otsu_____")

    is_forest_table = np.zeros((table_size, table_size))
    
    # loop through each block and save as a separate JPEG file
    col = 0
    row = 0
    for i in range(0, img.shape[0], block_size):  
        print("aaaaaaaaaaaaaaaaaaa")     
        for j in range(0, img.shape[1], block_size):  
            # calculate the pixel coordinates of the block
            ulx = i
            uly = j
            lrx = i + block_size
            lry = j + block_size

            # make sure the block is within the image bounds
            lrx, lry, ulx, uly = check_block_within_bounds(img.shape, 
                                                           block_size,
                                                           lrx, 
                                                           lry, 
                                                           ulx,
                                                           uly)

            block = img[ulx:lrx, uly:lry, :]

            predicted_label = predict_block(block, threshold)
            is_forest_table[col, row] = predicted_label
            row += 1
            print("bbbbbbbbbbbb")
        col += 1
        
        row = 0
    # print(is_forest_table)
    print("________in otsu 2________")
    for i in range(1, is_forest_table.shape[0] - 1):
        for j in range(1, is_forest_table.shape[1] - 1):
            
            current_predict = is_forest_table[i, j]

            if current_predict == 0:
                continue

            up_predict = is_forest_table[i-1, j]
            down_predict = is_forest_table[i+1, j]
            left_predict = is_forest_table[i, j-1]
            right_predict = is_forest_table[i, j+1]
            ulx = i * block_size
            uly = j * block_size
            lrx = i * block_size + block_size
            lry = j * block_size + block_size

            if right_predict == 0:
                block = img[ulx:lrx, uly + 32:lry + 32, :]
                is_forest_table[i, j+1] = predict_block(block, threshold)
                
            if left_predict == 0:
                block = img[ulx:lrx, uly - 32:lry - 32, :]
                # print("Left")
                # show_image(block)
                is_forest_table[i, j-1] = predict_block(block, threshold)

            if up_predict == 0:
                block = img[ulx-32:lrx-32, uly:lry, :]
                # print("Up")
                # show_image(block)
                is_forest_table[i-1, j] = predict_block(block, threshold)

            if down_predict == 0:
                block = img[ulx+32:lrx+32, uly:lry, :]
                # print("Down")
                # show_image(block)
                is_forest_table[i+1, j] = predict_block(block, threshold)
            
    # расматриваем частный случай на краях:
    top_left = is_forest_table[0, 0]
    print("________in otsu 3________")
    if top_left == 0:
        block_right = img[0:block_size, 32:block_size + 32, :]
        block_down = img[32:block_size + 32, 0:block_size, :]
        if predict_block(block_right, threshold) or predict_block(block_down, threshold):
            is_forest_table[0, 0] = 1

    top_right = is_forest_table[0, 1]
    if top_right == 0:
        block_left = img[0:block_size, img.shape[1] - block_size - 32:img.shape[1] - 32, :]
        block_down = img[32:block_size + 32, img.shape[1] - block_size:img.shape[1], :]
        
        if predict_block(block_left, threshold) or predict_block(block_down, threshold):
            is_forest_table[0, 1] = 1

    down_left = is_forest_table[1, 0]
    if down_left == 0:
        block_up = img[img.shape[0] - block_size - 32:img.shape[0] - 32, 0:block_size, :]
        block_right = img[img.shape[0] - block_size:img.shape[0], 32:block_size + 32, :]

        if predict_block(block_up, threshold) or predict_block(block_right, threshold):
            is_forest_table[1, 0] = 1

    down_right = is_forest_table[1, 1]
    if down_right == 0:
        block_left = img[img.shape[0] - block_size:img.shape[0], img.shape[1] - block_size - 32:img.shape[1]-32, :]
        block_up = img[img.shape[0] - block_size-32:img.shape[0]-32, img.shape[1] - block_size:img.shape[1], :]
        if predict_block(block_left, threshold) or predict_block(block_up, threshold):
            is_forest_table[1, 1] = 1

    #print(is_forest_table)
    col = 0
    row = 0
    for i in range(0, img.shape[0], block_size):
        for j in range(0, img.shape[1], block_size):
            # calculate the pixel coordinates of the block
            ulx = i
            uly = j
            lrx = i + block_size
            lry = j + block_size
            # make sure the block is within the image bounds
            lrx, lry, ulx, uly = check_block_within_bounds(img.shape,
                                                           block_size,
                                                           lrx, 
                                                           lry, 
                                                           ulx, 
                                                           uly)

            if is_forest_table[col, row] == 0:
                binary_image[ulx:lrx, uly:lry] = 0
            row += 1
        col += 1
        row = 0

    contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    update(37)
    return contours



def get_image_RGB(image_name, geotif_bytes):
    '''
    Преобразовывает tif файл в 3-х канальное 8-битное изображение и возвращает его, как массив numpy.
    
    geotif_bytes - путь до tif файла.
    '''
    gdal.FileFromMemBuffer("/vsimem/" + image_name, geotif_bytes)
    image = gdal.Open("/vsimem/" + image_name)

    # As, there are 3 bands, we will store in 3 different variables 
    band_1 = image.GetRasterBand(1) # red channel  
    band_2 = image.GetRasterBand(2) # green channel  
    band_3 = image.GetRasterBand(3) # blue channel   

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
    blurred_image = cv2.GaussianBlur(gray,(5,5),0)
    update(15)

    otsu_threshold, image_result = cv2.threshold(
        blurred_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU,
    )
    update(20)

    # Remove noise and fill holes in the binary image using morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
    update(25)

    closed = cv2.morphologyEx(image_result, cv2.MORPH_OPEN, kernel)
    update(30)

    # Find the contours in the input image
    #contours, hierarchy = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)
    return closed
    



