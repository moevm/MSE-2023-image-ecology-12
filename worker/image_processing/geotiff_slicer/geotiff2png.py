from osgeo import gdal


def geotiffToPng(geotiffName, pngName, optionsList = ['-ot Byte', '-of PNG', '-b 1', '-scale']):
    """
    Function to convert geotiff file to png.
    - pngName - path to store output png.
    - geotiffName - path to geotiff image to convert.
    - options - list of options to gdal.Translate.
    """
    gdal.Translate(
        pngName,
        geotiffName,
        options=" ".join(optionsList)
    )