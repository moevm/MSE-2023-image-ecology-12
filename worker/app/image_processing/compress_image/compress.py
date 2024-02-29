import rasterio
from rasterio.enums import Compression


def compress(input_geotiff_path: str, output_geotiff_path: str):
    with rasterio.open(input_geotiff_path) as src:
        profile = src.profile

        profile.update(compression=Compression.lzw)

        with rasterio.open(output_geotiff_path, 'w', **profile) as dst:
            for i in range(1, src.count + 1):
                data = src.read(i)
                dst.write(data, i)
