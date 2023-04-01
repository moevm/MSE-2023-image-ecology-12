FROM osgeo/gdal
RUN apt-get update
RUN apt install -y python3-pip
WORKDIR /app 
RUN pip install flask flask_cors pymongo gdal2tiles rasterio opencv-python sdd_segmentation
COPY . .
