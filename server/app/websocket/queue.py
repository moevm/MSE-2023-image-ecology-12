from app import app, socketio
from app.db import get_redis
from redis.client import StrictRedis
from werkzeug.local import LocalProxy

redis: StrictRedis = LocalProxy(get_redis)


def send_queue():
    with app.app_context():
        queue = []
        for i in redis.keys('queue:*'):
            queue.append(redis.hgetall(i))
        socketio.emit('queue', queue)
