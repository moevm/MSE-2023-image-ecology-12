from rasterio.mask import mask
import geopandas as gpd
from shapely.geometry import box
from rasterio.io import MemoryFile

def crop_image(input_bytes: bytes, minx: int, miny: int, maxx: int, maxy: int) -> bytes:
    bbox = box(minx, miny, maxx, maxy)
    geo = gpd.GeoDataFrame({'geometry': bbox}, index=[0], crs="EPSG:4326")

    with MemoryFile(input_bytes) as memfile:
        with memfile.open() as src:
            geo = geo.to_crs(src.crs)
            out_image, out_transform = mask(src, geo.geometry, crop=True)
            out_meta = src.meta.copy()
        out_meta.update({
            "driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform
        })

    # Создание нового MemoryFile для записи выходных данных
    with MemoryFile() as mem_dst:
        with mem_dst.open(**out_meta) as dest:
            dest.write(out_image)

        # Получаем выходные данные в виде массива байт
        output_bytes = mem_dst.read()

    return output_bytes