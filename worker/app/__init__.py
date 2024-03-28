from app import config
from celery import Celery

app = Celery(include=['app.tasks.image_process', 'app.tasks.slice', 'app.tasks.dev'])
app.conf.broker_url = config.REDIS_URI
app.conf.result_backend = config.REDIS_URI
