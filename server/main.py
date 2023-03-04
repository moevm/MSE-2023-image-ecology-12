from flask import Flask
from flask_pymongo import PyMongo
import requests
import os
import random

# Ссылка на базу
dbUri = os.environ['DB_URI'] if ('DB_URI' in os.environ) else "mongodb://localhost:27017/db"
print(f'DB URI: {dbUri}')

# Ссылка на рабочий процесс
workerUri = os.environ['WORKER_URI'] if ('WORKER_URI' in os.environ) else "http://localhost:5001/"
print(f'DB URI: {workerUri}')

# Flask приложение
app = Flask(__name__)
app.config["MONGO_URI"] = dbUri
mongo = PyMongo(app)

# Добавим тестовые данные
db = mongo.db
testCollection = mongo.db.test_collection
item = {"test_field": random.randint(0, 100)}
testCollection.insert_one(item)


# Тестовый маршрут, возвращает ответ воркера и всю тестовую коллекцию
@app.route("/api")
def home_page():
    entries = mongo.db.test_collection.find({})
    workerRes = requests.get(workerUri)
    return f'Worker response: {workerRes.text} | \n {str(list(entries))}'


port = os.environ['FLASK_PORT'] if ('FLASK_PORT' in os.environ) else 5005
# Запуск приложения
app.run(host='0.0.0.0', port=port)