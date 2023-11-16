from celery import Celery
from app import config

app = Celery(include=['app.tasks.image_process', 'app.tasks.slice', 'app.tasks.dev', 'app.tasks.download_images'])
app.conf.broker_url = config.REDIS_URI
app.conf.result_backend = config.REDIS_URI
