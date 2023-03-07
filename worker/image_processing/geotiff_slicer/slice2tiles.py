import os
import gdal2tiles
import rasterio
from osgeo import gdal


def sliceToTiles(geotiffPath,
        slicesOutputPath,
        optionsTranslate = ['-ot Byte', '-b 1', '-of vrt', '-scale'],
        optionsSliceToTiles = {}):
    """
    Function that prepares and cuts a geotiff file into fragments that are available for display in leaflet.js.
    - geotiffPath - path to geotiff file for preparing and slicing.
    - slicesOutputPath - path to the directory where the received slices will be stored.
    - optionsTranslate - list of options for gdal_translate (Translate options to convert 16 bit images to 8 bit).
    - optionsSliceToTiles - dict of options for slicing (for gdal2tiles).
    """
    _preprocessGeotiff(geotiffPath, optionsTranslate)
    _slicePreprocessedGeotiff(geotiffPath[:geotiffPath.rfind('.')] + '.vrt', slicesOutputPath, optionsSliceToTiles)
    os.remove(geotiffPath[:geotiffPath.rfind('.')] + '.vrt')

def _preprocessGeotiff(
        geotiffPath,
        optionsTranslate
    ):
    """
    Function which converts geotiff files into a shape with the possibility of successful slicing (and save res to .vrt).
    - geotiffPath - path to geotiff file for preprocessing.
    - optionsTranslate - options for gdal.Translate (Translate options to convert 16 bit images to 8 bit).
    """
    # Translate and create new vrt file
    gdal.Translate(geotiffPath[:geotiffPath.rfind('.')] + '.vrt', 
                   geotiffPath, 
                   options=" ".join(optionsTranslate)
                  )


def _slicePreprocessedGeotiff(
        geotiffPath,
        slicesOutputPath,
        optionsSliceToTiles
    ):
    """
    Function that cuts a geotiff file into fragments that are available for display in leaflet.js.
    - geotiffPath - path to geotiff file for slicing.
    - slicesOutputPath - path to the directory where the received slices will be stored.
    - optionsSliceToTiles - options for slicing (for gdal2tiles). 
    """
    if not os.path.exists(slicesOutputPath):
        os.makedirs(slicesOutputPath)
    gdal2tiles.generate_tiles(geotiffPath, slicesOutputPath, **optionsSliceToTiles)
