# Dockerfile para backend FastAPI
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y portaudio19-dev gcc
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
