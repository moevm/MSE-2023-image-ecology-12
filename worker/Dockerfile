FROM osgeo/gdal:ubuntu-small-3.6.3

WORKDIR /worker

RUN apt-get update && apt-get install ffmpeg=7:4.4.2-0ubuntu0.22.04.1 libsm6=2:1.2.3-1build2 libxext6=2:1.3.4-1build1 -y && apt install -y python3-pip && python -m pip install pip==22.0.2

ADD requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY app app
