import os
import gdal2tiles
from osgeo import gdal


# -b это слой, который берем, порядок слоев 1, 2, 3 так как sample.tif в формате rgb.
def sliceToTiles(
        geotiffName,
        geotiffBytes,
        slicesOutputPath,
        optionsTranslate = ['-if GTiff', '-ot Byte', '-b 1', '-b 2', '-b 3', '-of vrt', '-scale'],
        optionsSliceToTiles = {"nb_processes": 96}
    ):
    """
    Function that prepares and cuts a geotiff file into fragments that are available for display in leaflet.js.
    - geotiffName - name of geotiff file for preparing and slicing.
    - geotiffBytes - byte array of geotiff file for preparing and slicing.
    - optionsTranslate - list of options for gdal_translate (Translate options to convert 16 bit images to 8 bit).
    - optionsSliceToTiles - dict of options for slicing (for gdal2tiles).
    """
    gdal.FileFromMemBuffer("/vsimem/img.tiff", geotiffBytes)
    image = gdal.Open("/vsimem/img.tiff")

    _preprocessGeotiff(geotiffName, image, optionsTranslate)
    _slicePreprocessedGeotiff(geotiffName[:geotiffName.rfind('.')] + '.vrt', slicesOutputPath, optionsSliceToTiles)
    os.remove(geotiffName[:geotiffName.rfind('.')] + '.vrt')
    gdal.Unlink("/vsimem/img.tiff")

def _preprocessGeotiff(
        geotiffName,
        geotiffDataset,
        optionsTranslate
    ):
    """
    Function which converts geotiff files into a shape with the possibility of successful slicing (and save res to .vrt).
    - geotiffName - name of geotiff file for preparing.
    - geotiffDataset - gdal dataset of geotiff file for preparing.
    - optionsTranslate - options for gdal.Translate (Translate options to convert 16 bit images to 8 bit).
    """
    # Translate and create new vrt file
    gdal.Translate(geotiffName[:geotiffName.rfind('.')] + '.vrt', 
                   geotiffDataset, 
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
