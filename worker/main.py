from flask import Flask
from flask_pymongo import PyMongo
import os

# Ссылка на базу
dbUri = os.environ['DB_URI'] if ('DB_URI' in os.environ) else "mongodb://localhost:27017/db"
print(f'DB URI: {dbUri}')

# Flask приложение
app = Flask(__name__)
app.config["MONGO_URI"] = dbUri
mongo = PyMongo(app)


# Возвращаем ответ рабочего процесса (количество записей в базе)
@app.route("/")
def home_page():
    entries = mongo.db.test_collection.find({})
    return f'collections length - {len(list(entries))}'


port = os.environ['FLASK_PORT'] if ('FLASK_PORT' in os.environ) else 5001
# Запуск приложения
app.run(host='0.0.0.0', port=port)
