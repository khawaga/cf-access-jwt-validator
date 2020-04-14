FROM python:3.7-slim

ENV PYTHONUNBUFFERED=1
ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0:8080 --access-logfile=-"

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "main:app"]
