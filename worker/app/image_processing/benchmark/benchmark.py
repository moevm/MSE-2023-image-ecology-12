import time
import glob
import rasterio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from image_processing.compress_image.compress import compress
from image_processing.crop_image.crop import crop_image


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

        print(f"{operation.__name__} для {file_path} заняло {elapsed_time:.4f} секунд")

    return sum(times) / len(times)


if __name__ =="__main__":
    geotiff_files = glob.glob("../map_samples/*.tif")

    avg_crop_time = benchmark(geotiff_files, crop_image, 0, 0, 1000, 1000)
    print(f"Среднее время обрезки: {avg_crop_time:.4f} секунд")

    avg_compress_time = benchmark(geotiff_files, compress)
    print(f"Среднее время сжатия: {avg_compress_time:.4f} секунд")
