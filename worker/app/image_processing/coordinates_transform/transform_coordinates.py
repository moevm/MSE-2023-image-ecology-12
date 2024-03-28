import rasterio.warp
from rasterio.crs import CRS


class CoordintesTransformer:
    '''
    Класс для преобразования координат tif изображения. В конеце использования должен быть вызван метод close.

    geotif_bytes - байтовый массив tif файла.
    '''

    def __init__(self, geotif_bytes: bytes):
        self.image_file = rasterio.MemoryFile(geotif_bytes)
        self.image = self.image_file.open()
        self.lat_long_crs = CRS.from_epsg(4326)
        self.image_crs = self.image.crs

    def pixel_xy_to_lat_long(self, x, y):
        xy_in_image_crs = self.image.xy(y, x)
        if self.image_crs != self.lat_long_crs:
            long_lat = rasterio.warp.transform(
                self.image_crs, self.lat_long_crs, [xy_in_image_crs[0]], [xy_in_image_crs[1]]
            )
            # return [lattitude, longitude]
            return long_lat[1][0], long_lat[0][0]
        # return [lattitude, longitude]
        return xy_in_image_crs[1], xy_in_image_crs[0]

    def close(self):
        self.image.close()
        self.image_file.close()
