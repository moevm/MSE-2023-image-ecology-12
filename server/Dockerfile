FROM osgeo/gdal:ubuntu-small-3.6.3

RUN apt-get update && apt install -y python3-pip && python -m pip install pip==22.0.2

ADD ./requirements.txt /server/requirements.txt

RUN pip install -r /server/requirements.txt

COPY . /server
