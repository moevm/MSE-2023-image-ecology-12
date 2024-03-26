import time
import glob
import sys
import os
import warnings
from rasterio.errors import NodataShadowWarning

warnings.filterwarnings("ignore", category=NodataShadowWarning)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from image_processing.compress_image.compress import compress
from image_processing.crop_image.crop import crop_image


def read_geotiff(file_path):
    with open(file_path, "rb") as f:
        return f.read()


def get_file_size(file_path):
    return os.path.getsize(file_path)


def weighted_avg(times: float, weights: float) -> float:
    if len(times) == 0:
        return float("+inf")
    return sum(t * w for t, w in zip(times, weights)) / sum(weights)


def avg(arr: list) -> float:
    if len(arr) == 0:
        return float("+inf")
    return sum(arr) / len(arr)


def time_to_measure_time():
    s = time.time_ns()
    e = time.time_ns()
    return e - s


def benchmark(files, operation, *args, n_runs=10, **kwargs):
    times = []
    weights = []

    for file_path in files:
        file_times = []
        file_size = get_file_size(file_path)
        weights.append(file_size)

        for _ in range(n_runs):
            input_bytes = read_geotiff(file_path)

            start_time = time.time_ns()
            output_bytes = operation(input_bytes, *args, **kwargs)
            end_time = time.time_ns()

            elapsed_time = end_time - start_time
            file_times.append(elapsed_time)

            print(
                f"{operation.__name__} выполнение {len(file_times)} для {file_path} заняло {elapsed_time} наносекунд (размер файла {file_size} байт)"
            )

        time_delations = [time_to_measure_time() for _ in range(n_runs)]

        avg_time_delation = avg(time_delations)
        avg_file_time = avg(file_times)
        times.append(avg_file_time - avg_time_delation)
        print(f"Среднее время для {file_path}: {avg_file_time:.4f} наносекунд\n")
    return weighted_avg(times, weights)


if __name__ == "__main__":
    geotiff_files = glob.glob("../map_samples/*.tif")
    print(geotiff_files)
    avg_crop_time = benchmark(geotiff_files, crop_image, 0, 0, 1000, 1000, n_runs=10)
    print(f"Среднее время обрезки: {avg_crop_time:.4f} наносекунд")

    avg_compress_time = benchmark(geotiff_files, compress)
    print(f"Среднее время сжатия: {avg_compress_time:.4f} наносекунд")
