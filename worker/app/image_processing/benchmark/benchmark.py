import time
import glob
import rasterio

from ..compress_image.compress import compress
from ..crop_image.crop import crop_image


def read_geotiff(file_path):
    with open(file_path, "rb") as f:
        return f.read()


def benchmark(files, operation, *args, **kwargs):
    times = []

    for file_path in files:
        input_bytes = read_geotiff(file_path)

        start_time = time.time()

        output_bytes = operation(input_bytes, *args, **kwargs)

        end_time = time.time()

        elapsed_time = end_time - start_time
        times.append(elapsed_time)

        print(f"{operation.name} для {file_path} заняло {elapsed_time:.4f} секунд")

    return sum(times) / len(times)


geotiff_files = glob.glob("geotiff_files/*.tif")

avg_crop_time = benchmark(geotiff_files, crop_image, 0, 0, 100, 100)
print(f"Среднее время обрезки: {avg_crop_time:.4f} секунд")

avg_compress_time = benchmark(geotiff_files, compress)
print(f"Среднее время сжатия: {avg_compress_time:.4f} секунд")
