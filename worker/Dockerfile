FROM osgeo/gdal:ubuntu-small-3.6.3
RUN apt-get update && apt install -y python3-pip
WORKDIR /app 
RUN pip install flask flask_cors pymongo gdal2tiles rasterio opencv-python sdd_segmentation
COPY . .
