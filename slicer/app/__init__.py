from celery import Celery
from app import config

app = Celery(include=['app.tasks.slice'])
app.conf.broker_url = config.REDIS_URI
app.conf.result_backend = config.REDIS_URI
