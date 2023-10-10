import cv2
import numpy as np
from osgeo import gdal
from app.db import local


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


def morph_operations(image_arr, use_gaussian_filter: bool = True):
    if use_gaussian_filter:
        # denoise the image with a Gaussian filter
        image_arr = cv2.GaussianBlur(image_arr, (5, 5), 0)

    # Remove noise and fill holes in the binary image using morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
    return cv2.morphologyEx(image_arr, cv2.MORPH_OPEN, kernel)


def connected_components(threshold, threshold_area=250, threshold_width=50, threshold_height=50, connectivity=8):
    # perform connected component analysis
    # apply connected component analysis to the thresholded image
    output = cv2.connectedComponentsWithStats(threshold, connectivity, cv2.CV_32S)
    (numLabels, labels, stats, centroids) = output
    # initialize an output mask to store all forests parsed from
    # the image
    mask = np.zeros(threshold.shape, dtype="uint8")
    # loop over the number of unique connected component labels

    for i in range(1, numLabels):
        # extract the connected component statistics and centroid for the current label
        x = stats[i, cv2.CC_STAT_LEFT]
        y = stats[i, cv2.CC_STAT_TOP]
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]
        area = stats[i, cv2.CC_STAT_AREA]
        # ensure the width, height, and area are all neither too small
        # nor too big
        keepWidth = w > threshold_width
        keepHeight = h > threshold_height
        keepArea = area > threshold_area
        # (cX, cY) = centroids[i]
        # ensure the connected component we are examining passes all
        # three tests
        if all((keepWidth, keepHeight, keepArea)):
            componentMask = (labels == i).astype("uint8")  # * 255
            mask = cv2.bitwise_or(mask, componentMask)
            # mask[y:y + h, x:x + w, :] = threshold[y:y + h, x:x + w, :]
    return mask


def find_contours(thresh):
    # Find the contours in the input image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)
    # Аппроксимируем контур, чтобы уменьшить число точек.
    contours_approx = []
    for line in contours:
        # Преобразовываем координаты каждой точки из пикселей в широту и долготу.
        eps = 0.0001 * cv2.arcLength(line, True)
        line_approx = cv2.approxPolyDP(line, eps, True)
        contours_approx.append(line_approx)
    return contours_approx


def connected_components_for_points(closed, connectivity=2):
    # the furthest points of components
    point_cords = []

    # perform connected component analysis
    # apply connected component analysis to the thresholded image
    output = cv2.connectedComponentsWithStats(closed, connectivity, cv2.CV_32S)
    (numLabels, labels, stats, centroids) = output
    # loop over the number of unique connected component labels
    for i in range(1, numLabels):
        # extract the connected component statistics and centroid for
        # the current label
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]
        area = stats[i, cv2.CC_STAT_AREA]
        # ensure the width, height, and area are all neither too small
        # nor too big
        keepWidth = w > 128
        keepHeight = h > 128
        keepArea = area > 256
        (cX, cY) = centroids[i]
        # ensure the connected component we are examining passes all
        # three tests
        if all((keepWidth, keepHeight, keepArea)):
            # Calculate the distance transform
            componentMask = (labels == i).astype("uint8") * 255
            dist_transform = cv2.distanceTransform(componentMask, cv2.DIST_L2, 3)

            # Find the maximum distance and its corresponding coordinates
            max_distance = np.amax(dist_transform)
            furthest_indices = np.unravel_index(np.argmax(dist_transform), dist_transform.shape)
            furthest_x, furthest_y = furthest_indices[1], furthest_indices[0]

            point_cords.append((int(furthest_x), int(furthest_y)))

    return point_cords


def check_block_within_bounds(shape, block_size, lrx, lry, ulx, uly):
    x_shape, y_shape = shape[0], shape[1]

    if lrx > x_shape:
        lrx = x_shape
        ulx = lrx - block_size
    if lry > y_shape:
        lry = y_shape
        uly = lry - block_size

    return lrx, lry, ulx, uly


def predict_block(block, threshold):
    input_size = (64, 64)
    image = cv2.resize(block, input_size)
    image = image.astype('float32') / 255.0

    prediction = local.model_forest.predict(np.expand_dims(image, axis=0))
    predicted_label = 1 if prediction.item() >= threshold else 0

    return predicted_label


def otsu_method(image, is_gray=False, ksize=(10, 10)):
    # For debuging use cv2_imshow
    # Applying Otsu's method setting the flag value into cv.THRESH_OTSU.
    # Use a bimodal image as an input.
    # Optimal threshold value is determined automatically.
    if not is_gray:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh_binary = cv2.THRESH_BINARY_INV
    else:
        gray = image
        thresh_binary = cv2.THRESH_BINARY

    # denoise the image with a Gaussian filter
    blurred_image = cv2.GaussianBlur(gray,(5,5),0)

    _, image_result = cv2.threshold(
        blurred_image, 0, 255, thresh_binary + cv2.THRESH_OTSU,
    )

    # Remove noise and fill holes in the binary image using morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize)
    closed = cv2.morphologyEx(image_result, cv2.MORPH_OPEN, kernel)

    return closed


def find_forest(img):
    block_size = 64
    table_size_x = int(img.shape[0] / 64) + 1
    table_size_y = int(img.shape[1] / 64) + 1
    threshold = 0.25

    binary_image = otsu_method(img)

    is_forest_table = np.zeros((table_size_x, table_size_y))

    # loop through each block and save as a separate JPEG file
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

            block = img[ulx:lrx, uly:lry, :]

            predicted_label = predict_block(block, threshold)
            is_forest_table[col, row] = predicted_label
            row += 1
        col += 1
        row = 0
    # print(is_forest_table)

    for i in range(1, is_forest_table.shape[0] - 1):
        for j in range(1, is_forest_table.shape[1] - 1):

            current_predict = is_forest_table[i, j]

            if current_predict == 0:
                continue

            up_predict = is_forest_table[i - 1, j]
            down_predict = is_forest_table[i + 1, j]
            left_predict = is_forest_table[i, j - 1]
            right_predict = is_forest_table[i, j + 1]
            ulx = i * block_size
            uly = j * block_size
            lrx = i * block_size + block_size
            lry = j * block_size + block_size

            if right_predict == 0:
                block = img[ulx:lrx, uly + 32:lry + 32, :]
                is_forest_table[i, j + 1] = predict_block(block, threshold)

            if left_predict == 0:
                block = img[ulx:lrx, uly - 32:lry - 32, :]
                # print("Left")
                # show_image(block)
                is_forest_table[i, j - 1] = predict_block(block, threshold)

            if up_predict == 0:
                block = img[ulx - 32:lrx - 32, uly:lry, :]
                # print("Up")
                # show_image(block)
                is_forest_table[i - 1, j] = predict_block(block, threshold)

            if down_predict == 0:
                block = img[ulx + 32:lrx + 32, uly:lry, :]
                # print("Down")
                # show_image(block)
                is_forest_table[i + 1, j] = predict_block(block, threshold)

    # расматриваем частный случай на краях:
    top_left = is_forest_table[0, 0]
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
        block_left = img[img.shape[0] - block_size:img.shape[0], img.shape[1] - block_size - 32:img.shape[1] - 32, :]
        block_up = img[img.shape[0] - block_size - 32:img.shape[0] - 32, img.shape[1] - block_size:img.shape[1], :]
        if predict_block(block_left, threshold) or predict_block(block_up, threshold):
            is_forest_table[1, 1] = 1

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

    return binary_image
