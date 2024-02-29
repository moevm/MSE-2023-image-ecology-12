import rasterio
from rasterio.mask import mask
import geopandas as gpd
from shapely.geometry import box
import pycrs


def crop_image(input_geotiff_path: str, output_geotiff_path: str, minx: int, miny: int, maxx: int, maxy: int):
    bbox = box(minx, miny, maxx, maxy)
    geo = gpd.GeoDataFrame({'geometry': bbox}, index=[0], crs="EPSG:4326")
    with rasterio.open(input_geotiff_path) as src:
        geo = geo.to_crs(src.crs)
        out_image, out_transform = mask(src, geo.geometry, crop=True)
        out_meta = src.meta.copy()

    out_meta.update({
        "driver": "GTiff",
        "height": out_image.shape[1],
        "width": out_image.shape[2],
        "transform": out_transform
    })

    with rasterio.open(output_geotiff_path, "w", **out_meta) as dest:
        dest.write(out_image)
