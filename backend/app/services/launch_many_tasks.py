import time
from app.services.tasks import add

if __name__ == "__main__":
    num_tasks = 20  # Número de tareas a lanzar
    print(f"Launching {num_tasks} Celery tasks...")
    for i in range(num_tasks):
        add.delay(i, i+1)
        print(f"Task {i+1} launched: add({i}, {i+1})")
        time.sleep(0.2)  # Pequeño delay para ver la métrica subir gradualmente
    print("All tasks launched!") 