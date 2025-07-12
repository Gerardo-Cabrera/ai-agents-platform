from celery import Celery
import time
import os

# Usa la variable de entorno REDIS_URL para compatibilidad con Docker Compose
broker_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
app = Celery("tasks", broker=broker_url)

@app.task
def add(x, y):
    time.sleep(5)  # Simula una tarea que tarda
    return x + y 