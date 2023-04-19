from os import environ

FLASK_PORT = environ.get('FLASK_PORT', 5000)
MONGO_URI = environ.get('MONGO_URI', "mongodb://mongo:27017/db")
REDIS_URI = environ.get('DB_URI', "redis://redis:6379/0")

PRUNE_DB = environ.get('PRUNE_DB', False)
TEST_DATA = environ.get('TEST_DATA', False)
DEBUG = environ.get('DEBUG', True)
