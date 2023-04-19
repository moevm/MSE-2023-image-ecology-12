from celery import Celery
from server import config

app = Celery()
app.conf.broker_url = config.REDIS_URI
app.conf.result_backend = config.REDIS_URI
