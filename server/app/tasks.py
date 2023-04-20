from celery import Celery

from app import config

app = Celery(include=['app.tasks.slice', 'app.tasks.image_process', 'app.tasks.dev'])
app.conf.broker_url = config.REDIS_URI
app.conf.result_backend = config.REDIS_URI


@app.task(name='delete_all_data_in_db_and_fs')
def delete_all_data_in_db_and_fs():
    pass


@app.task(name='add_test_data_db')
def add_test_data_db():
    pass


@app.task(name='thresholding_otsu')
def thresholding_otsu(fs_id):
    pass


@app.task(name='slice')
def slice(fs_id):
    pass
