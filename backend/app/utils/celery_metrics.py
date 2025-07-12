import threading
import time
import redis
from prometheus_client import Gauge
import os

# Prometheus Gauge for Celery queue length
celery_queue_length = Gauge(
    "celery_queue_length",
    "Number of pending tasks in Celery queue",
    ["queue"]
)

# Configuración de Redis (ajusta si usas otro host/puerto/db)
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def update_celery_queue_length_periodically(queue_name="celery", interval=10):
    while True:
        try:
            length = redis_client.llen(queue_name)
            celery_queue_length.labels(queue=queue_name).set(length)
        except Exception as e:
            print(f"Error updating Celery queue length: {e}")
        time.sleep(interval)

def start_queue_length_updater(queue_name="celery", interval=10):
    t = threading.Thread(target=update_celery_queue_length_periodically, args=(queue_name, interval), daemon=True)
    t.start() 