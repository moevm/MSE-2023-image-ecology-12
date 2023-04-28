from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from .routes import api_bp
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.register_blueprint(api_bp, url_prefix="/api")
CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*")

from .websocket.queue import send_queue

scheduler = BackgroundScheduler()
scheduler.add_job(send_queue, 'interval', seconds=1)
scheduler.start()

# Раскоментируй эту строчку, если хочешь очистить базу данных при запуске сервера (тестовый режим).
# delete_all_data_in_db_and_fs(application, db)
# add_test_data_db(application, db, fs, worker_url)
