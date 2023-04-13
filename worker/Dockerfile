FROM osgeo/gdal:ubuntu-small-3.6.3
RUN apt-get update && apt install -y python3-pip
WORKDIR /app 
COPY . .
RUN pip install -r /app/requirements.txt
