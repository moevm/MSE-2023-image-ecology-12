import time
from os import listdir, makedirs

from abc import ABC, abstractmethod
from bson import ObjectId
from app import app
from app.image_processing.compress_image.compress import compress
from app.image_processing.crop_image.crop import crop_image
from app.db import local

import asf_search as asf


class ImageDownloader(ABC):
    def __init__(
        self, username: str, password: str, start_date: str, end_date: str, polygon: str
    ) -> None:
        self._username = username
        self._password = password
        self._start_date = start_date
        self._end_date = end_date
        self._polygon = polygon

    @abstractmethod
    def download(self):
        pass


class AlaskaImageDownloader(ImageDownloader):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def download_images(self):
        session = asf.ASFSession().auth_with_creds(
            username=self._username, password=self._password
        )

        results = asf.geo_search(
            intersectsWith=self._polygon
            or "POLYGON((-91.97 28.78,-88.85 28.78,-88.85 30.31,-91.97 30.31,-91.97 28.78))",
            platform=asf.PLATFORM.UAVSAR,
            start=self._start_date or "2010-01-01",
            end=self._end_date or "2010-02-01",
            processingLevel=asf.PRODUCT_TYPE.METADATA,
            maxResults=20,
        )

        makedirs("./satellite_images", exist_ok=True)
        results.download(path="./satellite_images", session=session, processes=10)


Downloader = AlaskaImageDownloader
username = ""
password = ""


@app.task(name="pipeline", queue="pipeline")
def pipeline():
    db = local.db
    map_fs = local.map_fs
    redis = local.redis

    Downloader(username, password, None, None, None).download_images()

    for file_name in listdir("./satellite_images"):
        with open(f"./satellite_images/{file_name}", "rb") as file:
            data = file.read()
        file_id = map_fs.put(data, filename=file_name, chunk_size=256 * 1024)
        item = {
            "tile_map_resource": None,
            "fs_id": file_id,
            "forest_polygon": None,
            "name": file_name,
            "ready": False,
            "sliced": False,
        }

        result = db.images.insert_one(item)
        img_id = result.inserted_id

        image_info = db.images.find_one(ObjectId(img_id))
        queue_item = f"queue:{img_id}"

        redis.hset(queue_item, "status", "processing")
        update = lambda x: redis.hset(queue_item, "progress", x)

        # Получаем саму картинку из GridFS.
        image_bytes = map_fs.get(ObjectId(image_info["fs_id"])).read()
        time.sleep(10)
        update(10)
        # redis.hset(queue_item, "status", "compressing")
        compresses_bytes = compress(image_bytes)
        time.sleep(10)
        update(20)
        # redis.hset(queue_item, "status", "cropping")
        cropped_byte = crop_image(compresses_bytes, 0, 0, 100, 100)
        update(30)
        time.sleep(10)
        redis.delete(f"slice_queue:{img_id}")
    # raise Exception(f">>>>>>>>>>>>>>>>>>>>>>>>>>>test<<<<<<<<<<<<<<<< {len(cropped_byte)}")
    return "Done"
