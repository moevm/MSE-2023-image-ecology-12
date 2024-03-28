from app import app
from app.tasks.image_process import thresholding_otsu
from app.db import local


@app.task(name='delete_all_data_in_db_and_fs', queue="dev")
def delete_all_data_in_db_and_fs():
    local.db.client.drop_database('ecologyDB')
    print('All database data deleted.')
