FROM python:3.12.6-slim-bullseye

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . /app

WORKDIR /app/src

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "-b", "0.0.0.0:8000"]
